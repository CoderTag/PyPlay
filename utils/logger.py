# utils/logger.py
import logging
import os
import sys
import traceback
import json
import functools
import asyncio
import threading
import time
from datetime import datetime
from typing import Optional, Dict, Any, Callable
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from pathlib import Path
from contextlib import contextmanager
import inspect

# Try to import dotenv for environment variable loading
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is optional

class CustomFormatter(logging.Formatter):
    """Custom formatter with color support for console output"""
    
    COLORS = {
        'DEBUG': '\033[94m',     # Blue
        'INFO': '\033[92m',      # Green
        'WARNING': '\033[93m',   # Yellow
        'ERROR': '\033[91m',     # Red
        'CRITICAL': '\033[1;91m', # Bold Red
        'RESET': '\033[0m'       # Reset
    }
    
    def format(self, record):
        log_message = super().format(record)
        if record.levelname in self.COLORS and sys.stdout.isatty():
            # Add color only if output is to a terminal
            return f"{self.COLORS[record.levelname]}{log_message}{self.COLORS['RESET']}"
        return log_message

class AsyncLogHandler(logging.Handler):
    """Handler that processes logs asynchronously to avoid blocking"""
    
    def __init__(self, capacity=1000):
        super().__init__()
        self.queue = asyncio.Queue(maxsize=capacity)
        self.handler_task = None
        self.stop_event = asyncio.Event()
        self.handlers = []
    
    def emit(self, record):
        # Put the record in the queue if possible, otherwise drop it
        try:
            # Handle both async and sync contexts
            if asyncio.get_event_loop().is_running():
                asyncio.create_task(self._async_emit(record))
            else:
                # Drop log if queue is full in non-async context
                if not self.queue.full():
                    self.queue.put_nowait(record)
        except Exception:
            self.handleError(record)
    
    async def _async_emit(self, record):
        try:
            await asyncio.wait_for(self.queue.put(record), timeout=0.1)
        except asyncio.TimeoutError:
            # Queue is full, log will be dropped
            pass
        except Exception:
            self.handleError(record)
    
    def add_handler(self, handler):
        """Add a regular handler that will process the queued logs"""
        self.handlers.append(handler)
    
    async def start_processing(self):
        """Start the async processing of logs"""
        self.handler_task = asyncio.create_task(self._process_logs())
        
    async def _process_logs(self):
        """Process logs from the queue"""
        while not self.stop_event.is_set() or not self.queue.empty():
            try:
                record = await asyncio.wait_for(self.queue.get(), timeout=0.5)
                for handler in self.handlers:
                    if record.levelno >= handler.level:
                        handler.emit(record)
                self.queue.task_done()
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                print(f"Error processing log record: {e}")
    
    async def stop_processing(self):
        """Stop the async processing of logs"""
        self.stop_event.set()
        if self.handler_task:
            await self.handler_task

class Logger:
    _instances = {}  # Cache for logger instances
    
    @classmethod
    def get_logger(cls, name=None):
        """Get or create a logger instance for the given name"""
        if name is None:
            # Get the calling module's name
            frame = inspect.stack()[1]
            module = inspect.getmodule(frame[0])
            name = module.__name__ if module else "root"
            
        if name in cls._instances:
            return cls._instances[name]
        
        instance = cls(name)
        cls._instances[name] = instance
        return instance
    
    def __init__(self, name="automation_framework"):
        self.name = name
        self.logger = logging.getLogger(name)
        
        # Prevent adding handlers multiple times
        if self.logger.handlers:
            return
            
        # Get log level from environment
        log_level_str = os.environ.get('LOG_LEVEL', 'INFO').upper()
        console_level_str = os.environ.get('CONSOLE_LOG_LEVEL', log_level_str).upper()
        file_level_str = os.environ.get('FILE_LOG_LEVEL', log_level_str).upper()
        
        # Map string to logging level
        level_map = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }
        
        log_level = level_map.get(log_level_str, logging.INFO)
        console_level = level_map.get(console_level_str, log_level)
        file_level = level_map.get(file_level_str, log_level)
        
        self.logger.setLevel(logging.DEBUG)  # Capture all logs, filter at handler level
        
        # Get log configuration from environment
        log_dir = os.environ.get('LOG_DIR', 'logs')
        max_file_size = int(os.environ.get('LOG_MAX_FILE_SIZE', 10 * 1024 * 1024))  # 10MB default
        backup_count = int(os.environ.get('LOG_BACKUP_COUNT', 5))
        json_format = os.environ.get('LOG_JSON_FORMAT', 'false').lower() == 'true'
        
        # Create logs directory if it doesn't exist
        Path(log_dir).mkdir(exist_ok=True)
        
        # Determine appropriate formatters
        if json_format:
            file_formatter = self._create_json_formatter()
        else:
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - [%(threadName)s] %(pathname)s:%(lineno)d - %(message)s'
            )
        
        console_formatter = CustomFormatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        
        # Create file handler with rotation
        log_filename = f"{name}_{datetime.now().strftime('%Y%m%d')}.log"
        log_file_path = os.path.join(log_dir, log_filename)
        
        # Use rotating file handler to limit file size
        file_handler = RotatingFileHandler(
            log_file_path, 
            maxBytes=max_file_size, 
            backupCount=backup_count
        )
        file_handler.setLevel(file_level)
        file_handler.setFormatter(file_formatter)
        
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(console_level)
        console_handler.setFormatter(console_formatter)
        
        # Set up async handling if enabled
        if os.environ.get('ASYNC_LOGGING', 'false').lower() == 'true':
            self.async_handler = AsyncLogHandler()
            self.async_handler.add_handler(file_handler)
            self.async_handler.add_handler(console_handler)
            self.logger.addHandler(self.async_handler)
            
            # Start async processing if in an async context
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    asyncio.create_task(self.async_handler.start_processing())
            except RuntimeError:
                # Not in async context, will start when needed
                pass
        else:
            # Synchronous logging
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)
        
        # Log initial setup
        self.logger.debug(f"Logger initialized with level={log_level_str}, "
                         f"console={console_level_str}, file={file_level_str}")
    
    def _create_json_formatter(self):
        """Create a JSON formatter for structured logging"""
        class JsonFormatter(logging.Formatter):
            def format(self, record):
                log_data = {
                    'timestamp': datetime.fromtimestamp(record.created).isoformat(),
                    'level': record.levelname,
                    'logger': record.name,
                    'message': record.getMessage(),
                    'thread': record.threadName,
                    'file': record.pathname,
                    'line': record.lineno
                }
                
                # Add exception info if available
                if record.exc_info:
                    log_data['exception'] = {
                        'type': record.exc_info[0].__name__,
                        'message': str(record.exc_info[1]),
                        'traceback': traceback.format_exception(*record.exc_info)
                    }
                
                # Add any extra attributes
                for key, value in record.__dict__.items():
                    if key not in ['args', 'asctime', 'created', 'exc_info', 'exc_text', 
                                  'filename', 'funcName', 'id', 'levelname', 'levelno', 
                                  'lineno', 'module', 'msecs', 'message', 'msg', 'name', 
                                  'pathname', 'process', 'processName', 'relativeCreated', 
                                  'stack_info', 'thread', 'threadName']:
                        try:
                            # Attempt to serialize the value
                            json.dumps({key: value})
                            log_data[key] = value
                        except (TypeError, OverflowError):
                            # If it can't be serialized, convert to string
                            log_data[key] = str(value)
                
                return json.dumps(log_data)
        
        return JsonFormatter()
    
    async def start_async_logging(self):
        """Start async logging if configured"""
        if hasattr(self, 'async_handler'):
            await self.async_handler.start_processing()
    
    async def stop_async_logging(self):
        """Stop async logging if configured"""
        if hasattr(self, 'async_handler'):
            await self.async_handler.stop_processing()
    
    def debug(self, message, *args, **kwargs):
        """Log a debug message"""
        self.logger.debug(message, *args, **kwargs)
    
    def info(self, message, *args, **kwargs):
        """Log an info message"""
        self.logger.info(message, *args, **kwargs)
    
    def warning(self, message, *args, **kwargs):
        """Log a warning message"""
        self.logger.warning(message, *args, **kwargs)
    
    def error(self, message, *args, **kwargs):
        """Log an error message"""
        self.logger.error(message, *args, **kwargs)
    
    def critical(self, message, *args, **kwargs):
        """Log a critical message"""
        self.logger.critical(message, *args, **kwargs)
    
    def exception(self, message, *args, exc_info=True, **kwargs):
        """Log an exception with traceback"""
        self.logger.exception(message, *args, exc_info=exc_info, **kwargs)
    
    @contextmanager
    def log_time(self, operation_name, level=logging.INFO):
        """Context manager to log execution time of a block of code"""
        start_time = time.time()
        yield
        elapsed_time = time.time() - start_time
        self.logger.log(level, f"{operation_name} completed in {elapsed_time:.4f} seconds")
    
    async def async_log_time(self, operation_name, level=logging.INFO):
        """Async context manager to log execution time"""
        class AsyncLogTime:
            def __init__(self, logger, operation_name, level):
                self.logger = logger
                self.operation_name = operation_name
                self.level = level
                
            async def __aenter__(self):
                self.start_time = time.time()
                return self
                
            async def __aexit__(self, exc_type, exc_val, exc_tb):
                elapsed_time = time.time() - self.start_time
                self.logger.log(self.level, f"{self.operation_name} completed in {elapsed_time:.4f} seconds")
        
        return AsyncLogTime(self.logger, operation_name, level)
    
    def log_decorator(self, level=logging.DEBUG):
        """Decorator to log function calls"""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                func_name = func.__name__
                self.logger.log(level, f"Calling {func_name} with args={args}, kwargs={kwargs}")
                start_time = time.time()
                try:
                    result = func(*args, **kwargs)
                    elapsed_time = time.time() - start_time
                    self.logger.log(level, f"{func_name} completed in {elapsed_time:.4f} seconds")
                    return result
                except Exception as e:
                    self.logger.exception(f"Exception in {func_name}: {str(e)}")
                    raise
            return wrapper
        return decorator
    
    def async_log_decorator(self, level=logging.DEBUG):
        """Decorator to log async function calls"""
        def decorator(func):
            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                func_name = func.__name__
                self.logger.log(level, f"Calling async {func_name} with args={args}, kwargs={kwargs}")
                start_time = time.time()
                try:
                    result = await func(*args, **kwargs)
                    elapsed_time = time.time() - start_time
                    self.logger.log(level, f"Async {func_name} completed in {elapsed_time:.4f} seconds")
                    return result
                except Exception as e:
                    self.logger.exception(f"Exception in async {func_name}: {str(e)}")
                    raise
            return wrapper
        return decorator
    
    def set_context(self, **context):
        """Add context information to all subsequent log messages from this logger"""
        # Create a filter to add the context
        class ContextFilter(logging.Filter):
            def __init__(self, context_data):
                super().__init__()
                self.context_data = context_data
                
            def filter(self, record):
                for key, value in self.context_data.items():
                    setattr(record, key, value)
                return True
        
        # Remove any existing context filters
        for handler in self.logger.handlers:
            for filter in handler.filters:
                if isinstance(filter, ContextFilter):
                    handler.removeFilter(filter)
        
        # Add the new context filter
        context_filter = ContextFilter(context)
        for handler in self.logger.handlers:
            handler.addFilter(context_filter)

# Create a global function for easy access
def get_logger(name=None):
    return Logger.get_logger(name)