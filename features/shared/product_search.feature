@shared @search @regression
Feature: Product Search Functionality
  As a user of the application
  I want to search for products using various criteria
  So that I can find relevant items quickly

  Background:
    Given the system has the following "{entity_type}":
      | id  | name           | category    | price  | stock |
      | 101 | Business Laptop| Electronics | 1299.99| 45    |
      | 102 | Gaming Laptop  | Electronics | 1799.99| 28    |
      | 103 | Wireless Mouse | Accessories | 24.99  | 150   |
      | 104 | USB-C Adapter  | Accessories | 19.99  | 200   |
      | 105 | Office Chair   | Furniture   | 249.99 | 15    |

  @web @mobile @smoke
  Scenario: Search for products by exact name
    When the user searches for "{search_term}"
    Then the search results should contain exactly "{count}" "{entity_type}"
    And the "{entity_type}" with "{attribute}" "{value}" should be in the results
    And the search execution time should be under "{time_limit}"

  @web @mobile @api
  Scenario Outline: Filter products by category
    When the user filters "{entity_type}" by "{filter_attribute}" "<filter_value>"
    Then the search results should contain <count> "{entity_type}"
    And all results should have "{attribute}" "<expected_value>"

    Examples:
      | filter_value | count |
      | Electronics  | 2     |
      | Accessories  | 2     |
      | Furniture    | 1     |

  @web @api
  Scenario: Search with price range filter
    When the user searches with the following filters:
      | filter_name | filter_value |
      | min_price   | {min_price}  |
      | max_price   | {max_price}  |
    Then the search results should contain "{count}" "{entity_type}"
    And all results should have "{attribute}" between "{min_value}" and "{max_value}"

  @mobile @api
  Scenario: Search with multiple combined filters
    When the user searches with the following filters:
      | filter_name | filter_value  |
      | category    | {category}    |
      | min_price   | {min_price}   |
      | max_price   | {max_price}   |
      | in_stock    | {stock_value} |
    Then the search results should contain "{count}" "{entity_type}"
    And all results should have "{attribute}" "{expected_value}"
    And all results should have "{attribute}" between "{min_value}" and "{max_value}"
    And all results should have "{attribute}" "{comparison_operator}" "{threshold_value}"

  @web @mobile @accessibility
  Scenario: Search results pagination
    When the user performs a search that returns all "{entity_type}"
    And the user sets the page size to "{page_size}"
    Then the "{page_number}" page should show "{item_count}" "{entity_type}"
    And the pagination control should show "{total_pages}" total pages
    When the user navigates to page "{page_number}"
    Then page "{page_number}" should show "{item_count}" "{entity_type}"
    When the user navigates to page "{page_number}"
    Then page "{page_number}" should show "{item_count}" "{entity_type}"

  @web @mobile @api @negative
  Scenario: Search with no matching results
    When the user searches for "{search_term}"
    Then the search results should be empty
    And an appropriate "{message_type}" message should be displayed

  @api @performance
  Scenario: Search API response time
    When "{request_count}" concurrent search requests are sent to the API
    Then the average response time should be under "{time_limit}"
    And the "{percentile}" percentile response time should be under "{time_limit}"
    And all responses should have appropriate "{header_type}" headers