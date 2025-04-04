@web @auth @regression
Feature: Web Login Functionality
  As a user of the web application
  I want to be able to log in with my credentials
  So that I can access my account and use the application features

  Background:
    Given the web application is open on the "{page_name}" page
    And the user has a valid account in the system

  @smoke @critical
  Scenario: Successful login with valid credentials
    When the user enters "{username}" in the "username" field
    And the user enters "{password}" in the "password" field
    And the user clicks the "{button_name}" button
    Then the user should be redirected to the "{destination_page}" page
    And the element "{element_name}" should display text "{expected_text}"

  @negative
  Scenario: Failed login with invalid password
    When the user enters "{username}" in the "username" field
    And the user enters "{password}" in the "password" field
    And the user clicks the "{button_name}" button
    Then an error message "{error_message}" should be displayed
    And the user should remain on the "{current_page}" page

  @negative
  Scenario: Failed login with invalid username
    When the user enters "{username}" in the "username" field
    And the user enters "{password}" in the "password" field
    And the user clicks the "{button_name}" button
    Then an error message "{error_message}" should be displayed
    And the user should remain on the "{current_page}" page

  @accessibility
  Scenario: Login form supports keyboard navigation
    When the user navigates through "{form_name}" form using Tab key
    Then the focus should move through elements in the following order:
      | element_name |
      | username     |
      | password     |
      | login_button |

  @security @data-retention
  Scenario: Remember me functionality
    When the user enters "{username}" in the "username" field
    And the user enters "{password}" in the "password" field
    And the user checks the "{checkbox_name}" checkbox
    And the user clicks the "{button_name}" button
    And the user closes the browser
    And the user reopens the browser and navigates to the application
    Then the user should be automatically logged in
    And the element "{element_name}" should display text "{expected_text}"

  @ux
  Scenario Outline: Password field shows and hides password
    When the user enters "<password>" in the "password" field
    Then the "password" field should have type "{input_type}"
    When the user clicks the "{toggle_element}" element
    Then the "password" field should have type "{toggled_type}"
    When the user clicks the "{toggle_element}" element again
    Then the "password" field should have type "{input_type}"

    Examples:
      | password      | input_type | toggled_type | toggle_element   |
      | Simple123     | password   | text         | password_toggle  |
      | Complex@456!  | password   | text         | password_toggle  |
      | SuperSecret#1 | password   | text         | password_toggle  |