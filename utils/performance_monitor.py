# utils/performance_monitor.py
import time
from datetime import datetime
import csv
import os
from typing import Dict, List, Any

class PerformanceMonitor:
    def __init__(self, output_file="performance_metrics.csv"):
        self.metrics = []
        self.output_file = os.path.join("reports", "performance", output_file)
        self.ensure_directory()
    
    def ensure_directory(self):
        """Ensure the directory exists"""
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
    
    def start_timer(self, name: str) -> Dict[str, Any]:
        """Start timing an operation"""
        return {
            "name": name,
            "start_time": time.time(),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def end_timer(self, timer: Dict[str, Any], success: bool = True, metadata: Dict[str, Any] = None) -> None:
        """End timing and record the metric"""
        end_time = time.time()
        duration = end_time - timer["start_time"]
        
        metric = {
            "name": timer["name"],
            "duration": duration,
            "success": success,
            "timestamp": timer["timestamp"]
        }
        
        if metadata:
            metric.update(metadata)
        
        self.metrics.append(metric)
        return metric
    
    def record_metric(self, name: str, value: float, metadata: Dict[str, Any] = None) -> None:
        """Record a metric without timing"""
        metric = {
            "name": name,
            "value": value,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        if metadata:
            metric.update(metadata)
        
        self.metrics.append(metric)
    
    def save_metrics(self) -> None:
        """Save metrics to CSV file"""
        if not self.metrics:
            return
        
        # Get all possible field names
        fieldnames = set()
        for metric in self.metrics:
            fieldnames.update(metric.keys())
        
        # Write to CSV
        with open(self.output_file, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=sorted(fieldnames))
            writer.writeheader()
            writer.writerows(self.metrics)