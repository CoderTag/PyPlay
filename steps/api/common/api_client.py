# api/api_client.py
import requests
import json
from typing import Dict, Any, Optional

class ApiClient:
    def __init__(self, base_url: str, headers: Dict[str, str] = None):
        self.base_url = base_url
        self.headers = headers or {}
        self.session = requests.Session()
        self.response = None
    
    def update_headers(self, headers: Dict[str, str]):
        """Update headers with new values"""
        self.headers.update(headers)
        return self
    
    def get(self, endpoint: str, params: Dict[str, Any] = None):
        """Perform GET request"""
        url = f"{self.base_url}{endpoint}"
        self.response = self.session.get(
            url, 
            headers=self.headers, 
            params=params
        )
        return self
    
    def post(self, endpoint: str, payload: Dict[str, Any] = None, json_payload: Dict[str, Any] = None):
        """Perform POST request"""
        url = f"{self.base_url}{endpoint}"
        self.response = self.session.post(
            url, 
            headers=self.headers,
            data=payload,
            json=json_payload
        )
        return self
    
    def put(self, endpoint: str, payload: Dict[str, Any] = None, json_payload: Dict[str, Any] = None):
        """Perform PUT request"""
        url = f"{self.base_url}{endpoint}"
        self.response = self.session.put(
            url, 
            headers=self.headers,
            data=payload,
            json=json_payload
        )
        return self
    
    def delete(self, endpoint: str):
        """Perform DELETE request"""
        url = f"{self.base_url}{endpoint}"
        self.response = self.session.delete(url, headers=self.headers)
        return self
    
    def get_status_code(self) -> int:
        """Get response status code"""
        return self.response.status_code if self.response else None
    
    def get_json_response(self) -> Dict[str, Any]:
        """Get JSON response"""
        return self.response.json() if self.response else None
    
    def get_text_response(self) -> str:
        """Get text response"""
        return self.response.text if self.response else None