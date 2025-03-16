# utils/schema_validation.py
from pydantic import BaseModel, Field, ValidationError
from typing import List, Optional, Dict, Any
import json

class ProductSchema(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    category: str
    in_stock: bool
    sku: str

class AddressSchema(BaseModel):
    street: str
    city: str
    state: Optional[str] = None
    zip: str
    country: str

class OrderSchema(BaseModel):
    id: int
    user_id: int
    products: List[Dict[str, Any]]
    total_price: float
    shipping_address: AddressSchema
    status: str

def validate_schema(data, schema_class):
    """Validate data against a schema"""
    try:
        validated_data = schema_class(**data)
        return True, None
    except ValidationError as e:
        return False, str(e)

def validate_response(response, schema_class):
    """Validate API response against a schema"""
    if isinstance(response, dict):
        return validate_schema(response, schema_class)
    elif isinstance(response, list) and len(response) > 0:
        valid, error = validate_schema(response[0], schema_class)
        return valid, error
    else:
        return False, "Empty or invalid response"