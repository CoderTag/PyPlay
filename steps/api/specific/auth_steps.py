# steps/api/specific/auth_steps.py

from pytest_bdd import given, when, then, parsers
import requests
import json
import time
from targets.api.services.auth_service import AuthService
from targets.api.helpers.request_builder import RequestBuilder
from targets.api.helpers.schema_validator import SchemaValidator

@given(parsers.parse('the "{endpoint_name}" endpoints are available'))
def verify_endpoints_available(api_client, endpoint_name):
    """Verify that the specified endpoints are available."""
    auth_service = AuthService(api_client)
    assert auth_service.are_endpoints_available(endpoint_name), f"{endpoint_name} endpoints are not available"

@given(parsers.parse('a user has a valid "{token_type}" token'))
def get_valid_token(api_client, token_type, context):
    """Get a valid token of the specified type and store it in the context."""
    auth_service = AuthService(api_client)
    token = auth_service.get_valid_token(token_type)
    context[f"{token_type}_token"] = token
    assert token is not None, f"Failed to get valid {token_type} token"

@given(parsers.parse('a user has an expired "{token_type}" token'))
def get_expired_token(api_client, token_type, context):
    """Get an expired token of the specified type and store it in the context."""
    auth_service = AuthService(api_client)
    expired_token = auth_service.get_expired_token(token_type)
    context[f"expired_{token_type}_token"] = expired_token
    assert expired_token is not None, f"Failed to get expired {token_type} token"

@when(parsers.parse('a "{http_method}" request is sent to "{endpoint_path}" with parameters:'))
def send_request_with_params(api_client, http_method, endpoint_path, table, context):
    """Send a request to the specified endpoint with the specified parameters."""
    params = {row["key"]: row["value"] for row in table}
    request_builder = RequestBuilder(api_client)
    
    # Replace placeholders in the request
    for key, value in params.items():
        if isinstance(value, str) and value.startswith('{') and value.endswith('}'):
            placeholder = value[1:-1]  # Remove the curly braces
            # Check if the value is in the context
            if placeholder in context:
                params[key] = context[placeholder]
    
    response = request_builder.send_request(http_method, endpoint_path, params)
    context["response"] = response

@when(parsers.parse('a "{http_method}" request is sent to "{endpoint_path}" with the "{token_name}" token'))
def send_request_with_token(api_client, http_method, endpoint_path, token_name, context):
    """Send a request to the specified endpoint with the specified token."""
    token = context.get(token_name)
    request_builder = RequestBuilder(api_client)
    headers = {"Authorization": f"Bearer {token}"}
    response = request_builder.send_request(http_method, endpoint_path, headers=headers)
    context["response"] = response

@when(parsers.parse('"{request_count}" "{http_method}" requests are sent to "{endpoint_path}" within "{time_period}"'))
def send_multiple_requests(api_client, request_count, http_method, endpoint_path, time_period, context):
    """Send multiple requests to the specified endpoint within the specified time period."""
    request_builder = RequestBuilder(api_client)
    responses = []
    count = int(request_count)
    
    # Parse time period (e.g., "1 minute" to seconds)
    value, unit = time_period.split()
    total_seconds = 0
    if unit.lower().startswith('min'):
        total_seconds = int(value) * 60
    elif unit.lower().startswith('sec'):
        total_seconds = int(value)
    
    # Calculate delay between requests to spread them evenly
    delay = total_seconds / count if count > 1 else 0
    
    for _ in range(count):
        response = request_builder.send_request(http_method, endpoint_path)
        responses.append(response)
        if delay > 0:
            time.sleep(delay)
    
    context["responses"] = responses

@then(parsers.parse('the response status code should be "{status_code}"'))
def verify_status_code(context, status_code):
    """Verify that the response status code matches the expected value."""
    response = context.get("response")
    assert response.status_code == int(status_code), f"Expected status code {status_code} but got {response.status_code}"

@then(parsers.parse('the response should contain a field "{field_name}" with type "{expected_type}"'))
def verify_field_type(context, field_name, expected_type):
    """Verify that the response contains a field of the specified type."""
    response = context.get("response")
    data = response.json()
    schema_validator = SchemaValidator()
    
    # Check if the field exists
    assert field_name in data, f"Field {field_name} not found in response"
    
    # Verify the field type
    result = schema_validator.validate_field_type(data, field_name, expected_type)
    assert result, f"Field {field_name} is not of type {expected_type}"

@then(parsers.parse('the response should contain field "{field_name}" with value "{expected_value}"'))
def verify_field_value(context, field_name, expected_value):
    """Verify that the response contains a field with the specified value."""
    response = context.get("response")
    data = response.json()
    
    # Navigate to nested fields using dot notation (e.g., "error.message")
    field_parts = field_name.split('.')
    current = data
    for part in field_parts:
        assert part in current, f"Field {part} not found in {current}"
        current = current[part]
    
    assert str(current) == expected_value, f"Expected {field_name} to be {expected_value} but got {current}"

@then(parsers.parse('the response should have header "{header_name}" with value "{header_value}"'))
def verify_header(context, header_name, header_value):
    """Verify that the response has a header with the specified value."""
    response = context.get("response")
    assert header_name in response.headers, f"Header {header_name} not found in response"
    assert response.headers[header_name] == header_value, f"Expected header {header_name} to be {header_value} but got {response.headers[header_name]}"

@then(parsers.parse('the response should have header "{header_name}"'))
def verify_header_exists(context, header_name):
    """Verify that the response has the specified header."""
    response = context.get("response")
    assert header_name in response.headers, f"Header {header_name} not found in response"