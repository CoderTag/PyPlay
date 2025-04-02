# utils/selector_loader.py
import json
import yaml
import os
import logging
import glob
from typing import Dict, Any
import asyncio
import time
from utils.logger import get_logger

# Get a logger for this module
logger = get_logger()


class SelectorLoader:
    _instance = None
    _selectors: Dict[str, Any] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SelectorLoader, cls).__new__(cls)
            cls._instance._selectors = cls._instance._load_selectors()
        return cls._instance
    
    def _load_selectors(self):
        """Load all selectors from multiple configuration files with environment suffix"""
        # logger = logging.getLogger(__name__)
        selectors_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "selectors")
        environment = os.environ.get('ENV', 'dev')
        
        # Dictionary to store all selectors
        all_selectors = {}
        
        # Find all JSON files with environment suffix
        json_pattern = os.path.join(selectors_dir, f"*_{environment}.json")
        json_files = glob.glob(json_pattern)
        
        # Find all YAML files with environment suffix
        yaml_pattern1 = os.path.join(selectors_dir, f"*_{environment}.yaml")
        yaml_pattern2 = os.path.join(selectors_dir, f"*_{environment}.yml")
        yaml_files = glob.glob(yaml_pattern1) + glob.glob(yaml_pattern2)
        
        # Combine all selector files
        all_files = json_files + yaml_files
        
        if not all_files:
            logger.warning(f"No selector files matching *_{environment}.json or *_{environment}.yaml/yml found in {selectors_dir}")
            
            # Fallback to a single selectors file if it exists
            for fallback_file in ["selectors.json", "selectors.yaml", "selectors.yml"]:
                default_file = os.path.join(selectors_dir, fallback_file)
                if os.path.exists(default_file):
                    logger.info(f"Using fallback selector file: {default_file}")
                    try:
                        with open(default_file, 'r') as file:
                            if fallback_file.endswith('.json'):
                                return json.load(file)
                            else:
                                return yaml.safe_load(file)
                    except Exception as e:
                        logger.error(f"Error loading fallback file {fallback_file}: {str(e)}")
            
            return {}
        
        # Load each file and merge into all_selectors
        for file_path in all_files:
            try:
                file_name = os.path.basename(file_path)
                file_extension = os.path.splitext(file_name)[1].lower()
                
                # Get page name by removing environment suffix and extension
                page_name = file_name.replace(f"_{environment}{file_extension}", "")
                
                logger.info(f"Loading selectors for '{page_name}' from {file_name}")
                
                with open(file_path, 'r') as file:
                    # Parse based on file extension
                    if file_extension == '.json':
                        selectors = json.load(file)
                    else:  # .yaml or .yml
                        selectors = yaml.safe_load(file)
                    
                    # If the file already has a top-level key structure, use it directly
                    if isinstance(selectors, dict) and len(selectors) == 1 and page_name in selectors:
                        all_selectors[page_name] = selectors[page_name]
                    else:
                        # Otherwise, use the entire file content for this page
                        all_selectors[page_name] = selectors
                        
            except (json.JSONDecodeError, yaml.YAMLError):
                logger.error(f"Error decoding {file_extension} from {file_path}")
            except Exception as e:
                logger.error(f"Error loading selector file {file_path}: {str(e)}")
        
        return all_selectors
    
    def get_selectors(self, page_name):
        """Get selectors for a specific page"""
        if not self._selectors:
            return {}
        return self._selectors.get(page_name, {})
    
    def reload_selectors(self):
        """Reload all selectors (useful during development)"""
        self._selectors = self._load_selectors()
        return self._selectors
    
    def list_available_pages(self):
        """List all available page names in the selector configuration"""
        return list(self._selectors.keys()) if self._selectors else []
    
    def validate_required_selectors(self, page_name, required_selectors):
        """
        Validate that all required selectors are present for a page
        
        Args:
            page_name: Name of the page to validate
            required_selectors: List of required selector names
            
        Returns:
            bool: True if all required selectors are present
            
        Raises:
            KeyError: If any required selectors are missing
        """
        page_selectors = self.get_selectors(page_name)
        missing = [selector for selector in required_selectors if selector not in page_selectors]
        
        if missing:
            raise KeyError(f"Required selectors missing for '{page_name}': {', '.join(missing)}")
        
        return True
    
    def get_selector_count(self):
        """Get a count of loaded selectors by page"""
        if not self._selectors:
            return {}
        
        return {page: len(selectors) for page, selectors in self._selectors.items()}
    
    def get_file_sources(self):
        """Return information about what files were loaded (for debugging)"""
        selectors_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "selectors")
        environment = os.environ.get('ENV', 'dev')
        
        json_pattern = os.path.join(selectors_dir, f"*_{environment}.json")
        yaml_pattern1 = os.path.join(selectors_dir, f"*_{environment}.yaml")
        yaml_pattern2 = os.path.join(selectors_dir, f"*_{environment}.yml")
        
        json_files = glob.glob(json_pattern)
        yaml_files = glob.glob(yaml_pattern1) + glob.glob(yaml_pattern2)
        
        return {
            "environment": environment,
            "json_files": [os.path.basename(f) for f in json_files],
            "yaml_files": [os.path.basename(f) for f in yaml_files],
            "selectors_directory": selectors_dir
        }