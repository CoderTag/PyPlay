# tests/step_defs/test_basic_navigation_steps.py
import pytest
from playwright.sync_api import Page, expect
from pytest_bdd import scenarios, given, when, then, parsers

# --- Setup ---
# Define the target feature files for these steps
# It looks for feature files relative to the step definition file's location
scenarios('../features/basic_navigation.feature')

# --- Constants ---
HOME_PAGE_URL = "https://www.pfizerforall.com/"
EXPECTED_TITLE = "Helping Patients Access Pfizer Medicines | Pfizer For All™"

# --- Step Definitions ---

# The decorator links this function to the Gherkin step
# Note: 'page' fixture is automatically available from pytest-playwright
@given('the user is on the Pfizer For All homepage')
def go_to_homepage(page: Page):
    """Navigates to the homepage."""
    print(f"\nNavigating to {HOME_PAGE_URL}")
    page.goto(HOME_PAGE_URL)
    print("Navigation complete.")

# 'parsers.parse' allows us to capture parts of the step text
# The captured value ('expected_title_from_feature') is passed as an argument
@then(parsers.parse('the page title should be "{expected_title_from_feature}"'))
def check_page_title(page: Page, expected_title_from_feature: str):
    """Verifies the page title."""
    print(f"Checking page title against: '{expected_title_from_feature}'")
    expect(page).to_have_title(expected_title_from_feature)
    print("Assertion passed: Page title is correct.")

# Example of how a 'When' step would look (we don't need one for this scenario)
# @when('the user performs some action')
# def perform_action(page: Page):
#     pass