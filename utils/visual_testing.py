# utils/visual_testing.py
import os
import base64
import requests
from typing import Dict, Any

def compare_visual(screenshot, name: str) -> Dict[str, Any]:
    """
    Compare screenshot with baseline using Testim
    
    Args:
        screenshot: Screenshot bytes or base64 string
        name: Unique identifier for the baseline
    
    Returns:
        Dict containing comparison results
    """
    # Convert screenshot to base64 if it's not already
    if isinstance(screenshot, bytes):
        screenshot_b64 = base64.b64encode(screenshot).decode('utf-8')
    else:
        screenshot_b64 = screenshot
    
    # Testim API endpoint
    testim_url = os.environ.get("TESTIM_API_URL")
    testim_project = os.environ.get("TESTIM_PROJECT_ID")
    testim_token = os.environ.get("TESTIM_API_TOKEN")
    
    # Prepare payload
    payload = {
        "projectId": testim_project,
        "baselineName": name,
        "screenshotBase64": screenshot_b64,
        "tolerance": 0.01  # 1% tolerance
    }
    
    # Call Testim API
    response = requests.post(
        f"{testim_url}/compare",
        headers={
            "Authorization": f"Bearer {testim_token}",
            "Content-Type": "application/json"
        },
        json=payload
    )
    
    # Parse and return results
    result = response.json()
    
    # If baseline doesn't exist, create it
    if response.status_code == 404:
        create_baseline(screenshot_b64, name)
        return {"status": "baseline_created", "message": "New baseline created"}
    
    return {
        "status": "match" if result.get("matched", False) else "mismatch",
        "diff_percentage": result.get("diffPercentage", 0),
        "diff_areas": result.get("diffAreas", [])
    }

def create_baseline(screenshot_b64: str, name: str) -> Dict[str, Any]:
    """Create a new baseline image"""
    # Testim API endpoint
    testim_url = os.environ.get("TESTIM_API_URL")
    testim_project = os.environ.get("TESTIM_PROJECT_ID")
    testim_token = os.environ.get("TESTIM_API_TOKEN")
    
    # Prepare payload
    payload = {
        "projectId": testim_project,
        "baselineName": name,
        "screenshotBase64": screenshot_b64
    }
    
    # Call Testim API
    response = requests.post(
        f"{testim_url}/baselines",
        headers={
            "Authorization": f"Bearer {testim_token}",
            "Content-Type": "application/json"
        },
        json=payload
    )
    
    # Parse and return results
    return response.json()