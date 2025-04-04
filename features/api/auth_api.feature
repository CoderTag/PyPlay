@api @auth @regression
Feature: Authentication API Endpoints
  As a developer integrating with the system
  I want to authenticate users via the API
  So that they can access protected resources

  Background:
    Given the API base URL is configured
    And the "{endpoint_name}" endpoints are available

  @smoke @critical
  Scenario: Generate JWT token with valid credentials
    When a "{http_method}" request is sent to "{endpoint_path}" with parameters:
      | key      | value          |
      | username | {username}     |
      | password | {password}     |
    Then the response status code should be "{status_code}"
    And the response should contain a field "{field_name}" with type "{expected_type}"
    And the "{token_field}" expiration time should be "{time_period}" from now
    And the response should have header "{header_name}" with value "{header_value}"

  @negative
  Scenario: Attempt to generate token with invalid credentials
    When a "{http_method}" request is sent to "{endpoint_path}" with parameters:
      | key      | value          |
      | username | {username}     |
      | password | {password}     |
    Then the response status code should be "{status_code}"
    And the response should contain field "{field_name}" with value "{expected_value}"
    And the response should have header "{header_name}" with value "{header_value}"

  @security
  Scenario: Refresh token functionality
    Given a user has a valid "{token_type}" token
    And the user has a valid "{token_type}" token
    When a "{http_method}" request is sent to "{endpoint_path}" with the "{token_name}" token
    Then the response status code should be "{status_code}"
    And the response should contain a field "{field_name}" with type "{expected_type}"
    And the new token should have a different "{property_name}"
    And the old token should no longer be valid

  @negative @security
  Scenario: Attempt to refresh with expired refresh token
    Given a user has an expired "{token_type}" token
    When a "{http_method}" request is sent to "{endpoint_path}" with the expired "{token_name}" token
    Then the response status code should be "{status_code}"
    And the response should contain field "{field_name}" with value "{expected_value}"

  @security
  Scenario: Revoke active token
    Given a user has a valid "{token_type}" token
    When a "{http_method}" request is sent to "{endpoint_path}" with the "{token_name}" token
    Then the response status code should be "{status_code}"
    And attempting to use the "{token_state}" token should return "{status_code}"

  @rate-limiting @security
  Scenario: Token endpoint rate limiting
    When "{request_count}" "{http_method}" requests are sent to "{endpoint_path}" within "{time_period}"
    Then at least one response should have status code "{status_code}"
    And the response should contain header "{header_name}"

  @performance
  Scenario: Authentication API performance
    When "{request_count}" simultaneous "{http_method}" requests are sent to "{endpoint_path}" with valid credentials
    Then all successful responses should be returned within "{time_limit}"
    And no response should take longer than "{max_time_limit}"
    And at least "{success_percentage}" of the requests should succeed with status code "{status_code}"