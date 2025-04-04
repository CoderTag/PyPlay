@web @pfa @regression
Feature: Basic Website Navigation

  Scenario: Verify Pfizer For All Homepage Title
    Given the user is on the Pfizer For All homepage
    Then the page title should be "Helping Patients Access Pfizer Medicines | Pfizer For All™"