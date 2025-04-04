@mobile @auth @regression
Feature: Mobile App Login Functionality
  As a mobile app user
  I want to be able to log in with my credentials
  So that I can access my account and use the app features

  Background:
    Given the mobile app "{app_name}" is installed and launched
    And the user is on the "{screen_name}" screen
    And the user has a valid account in the system

  @smoke @critical @android @ios
  Scenario: Successful login with valid credentials
    When the user enters "{username}" in the "{field_name}" field
    And the user enters "{password}" in the "{field_name}" field
    And the user taps the "{button_name}" button
    Then the user should be navigated to the "{destination_screen}" screen
    And the "{element_name}" should be visible

  @negative @android @ios
  Scenario: Failed login with invalid password
    When the user enters "{username}" in the "{field_name}" field
    And the user enters "{password}" in the "{field_name}" field
    And the user taps the "{button_name}" button
    Then an error toast message "{error_message}" should be displayed
    And the user should remain on the "{current_screen}" screen

  @biometric @android
  Scenario: Login with fingerprint on Android
    When the user taps the "{button_name}" button
    And the system "{dialog_name}" dialog appears
    And the user authenticates with a valid "{auth_method}"
    Then the user should be navigated to the "{destination_screen}" screen

  @biometric @ios
  Scenario: Login with Face ID on iOS
    When the user taps the "{button_name}" button
    And the system "{dialog_name}" dialog appears
    And the user authenticates with "{auth_method}"
    Then the user should be navigated to the "{destination_screen}" screen

  @offline @android @ios
  Scenario: Attempt login while offline
    Given the device has "{connection_status}" connection
    When the user enters "{username}" in the "{field_name}" field
    And the user enters "{password}" in the "{field_name}" field
    And the user taps the "{button_name}" button
    Then an error message "{error_message}" should be displayed
    And an option to "{action_name}" should be available

  @security @android @ios
  Scenario: User session timeout after inactivity
    Given the user is logged in
    When the app is in "{app_state}" for "{time_period}"
    And the user brings the app to "{app_state}"
    Then the user should be redirected to the "{destination_screen}" screen
    And a message "{message_text}" should be displayed

  @ux @android @ios
  Scenario Outline: Form validation for invalid inputs
    When the user enters "<username>" in the "username" field
    And the user enters "<password>" in the "password" field
    And the user taps the "{button_name}" button
    Then the error message "<error_message>" should be displayed
    
    Examples:
      | username     | password     | error_message                   |
      |              | mobile_pass  | Username is required            |
      | mobile_user  |              | Password is required            |
      | short        | mobile_pass  | Username must be at least 5 characters |
      | mobile_user  | short        | Password must be at least 8 characters |