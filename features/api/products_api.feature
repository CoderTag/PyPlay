# features/api_endpoints.feature
Feature: API Endpoints Testing
  As a developer
  I want to ensure all API endpoints work correctly
  So that the application functions properly

  Scenario: Get all products
    When I send a GET request to "/api/products"
    Then the response status code should be 200
    And the response should contain a list of products

  Scenario: Create a new order
    Given I have a valid auth token
    When I send a POST request to "/api/orders" with:
      """
      {
        "products": [
          {"id": 1, "quantity": 2},
          {"id": 3, "quantity": 1}
        ],
        "shipping_address": {
          "street": "123 Main St",
          "city": "Anytown",
          "zip": "12345"
        }
      }
      """
    Then the response status code should be 201
    And the response should contain the created order ID