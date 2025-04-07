@web @auth @regression
Feature: Web Login Functionality
  As a user of the web application
  I want to be able to log in with my credentials
  So that I can access my account and use the application features

  Background:
    Given the web application is open on the "{login > page_identifier}" page # Using identifier from login.yaml
    And the user has a valid account in the system

  @smoke @critical
  Scenario: Successful login with valid credentials
    When the user enters "{username}" in the "{login > username_field}" field
    And the user enters "{password}" in the "{login > password_field}" field
    And the user clicks the "{login > login_button}" button
    Then the user should be redirected to the "{homepage > dashboard_header}" page # Assumes homepage.yaml exists
    And the element "{homepage > welcome_message}" should display text "{expected_text}"

  @negative
  Scenario: Failed login with invalid password
    When the user enters "{username}" in the "{login > username_field}" field
    And the user enters "{invalid_password}" in the "{login > password_field}" field # Use specific value names
    And the user clicks the "{login > login_button}" button
    Then an error message "{login > error_message}" should be displayed # Reference error element
    And the text should be "{error_text}" # Separate step for text assertion is clearer
    And the user should remain on the "{login > page_identifier}" page

  # ... (Adapt other scenarios similarly) ...

  @accessibility
  Scenario: Login form supports keyboard navigation
    When the user navigates through "{login > login_form}" form using Tab key
    Then the focus should move through elements in the following order:
      | element_key        |
      | {login > username} | # Reference keys defined in YAML
      | {login > password} |
      | {login > login_button} |

  @security @data-retention
  Scenario: Remember me functionality
    When the user enters "{username}" in the "{login > username_field}" field
    And the user enters "{password}" in the "{login > password_field}" field
    And the user checks the "{login > remember_me_checkbox}" checkbox
    And the user clicks the "{login > login_button}" button
    And the user closes the browser
    And the user reopens the browser and navigates to the application
    Then the user should be automatically logged in
    And the element "{homepage > welcome_message}" should display text "{expected_text}"

   @ux
  Scenario Outline: Password field shows and hides password
    When the user enters "<password>" in the "{login > password_field}" field
    Then the "{login > password_field}" field should have attribute "type" with value "<input_type>" # Changed step
    When the user clicks the "{login > password_toggle}" element
    Then the "{login > password_field}" field should have attribute "type" with value "<toggled_type>" # Changed step
    When the user clicks the "{login > password_toggle}" element again
    Then the "{login > password_field}" field should have attribute "type" with value "<input_type>" # Changed step

    Examples:
      | password      | input_type | toggled_type |
      | Simple123     | password   | text         |