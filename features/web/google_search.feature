@web @google @regression
Feature: Google Search
  
  @search @smoke
  Scenario: Search for a keyword on Google
    Given the user is on the Google homepage
    When the user searches for "pytest-bdd"
    Then the search results should be displayed