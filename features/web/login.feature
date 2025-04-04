# features/login.feature
@login
Feature: User Authentication
  As a user
  I want to be able to log in to the application
  So that I can access my account

  Background:
    Given the user is on the login page

  @login
  Scenario: Successful login with valid credentials
    When the user enters username "valid_user"
    And the user enters password "valid_password"
    And the user clicks the login button
    Then the user should be redirected to the dashboard
    And the dashboard should display the user's name

  Scenario: Failed login with invalid credentials
    When the user enters username "invalid_user"
    And the user enters password "invalid_password"
    And the user clicks the login button
    Then an error message should be displayed
    And the user should remain on the login page

  @visual
  Scenario: Login page visual verification
    Then the login page should match the baseline