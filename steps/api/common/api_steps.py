# step_definitions/api_steps.py
import json
import pytest
from pytest_bdd import given, when, then, parsers
from steps.api.specific.endpoints import Endpoints

@given("I have a valid auth token")
def valid_auth_token(api_context, config):
    # Get a valid auth token
    response = api_context.post(
        Endpoints.LOGIN,
        json_payload={
            "username": config["users"]["valid_user"]["username"],
            "password": config["users"]["valid_user"]["password"]
        }
    ).get_json_response()
    
    token = response.get("token")
    assert token, "Failed to get authentication token"
    
    # Set the token in the headers
    api_context.update_headers({"Authorization": f"Bearer {token}"})

@when(parsers.parse('I send a GET request to "{endpoint}"'))
def send_get_request(api_context, endpoint):
    api_context.get(endpoint)

@when(parsers.parse('I send a POST request to "{endpoint}" with:'))
def send_post_request_with_payload(api_context, endpoint, text):
    payload = json.loads(text)
    api_context.post(endpoint, json_payload=payload)

@then(parsers.parse('the response status code should be {status:d}'))
def verify_status_code(api_context, status):
    assert api_context.get_status_code() == status, f"Expected status {status}, got {api_context.get_status_code()}"

@then("the response should contain a list of products")
def verify_products_list(api_context):
    response = api_context.get_json_response()
    assert isinstance(response, list), "Response is not a list"
    assert len(response) > 0, "Product list is empty"
    assert "id" in response[0], "Product doesn't have an ID"
    assert "name" in response[0], "Product doesn't have a name"

@then("the response should contain the created order ID")
def verify_order_id(api_context):
    response = api_context.get_json_response()
    assert "id" in response, "Response doesn't contain order ID"
    assert isinstance(response["id"], (int, str)), "Order ID is not valid"