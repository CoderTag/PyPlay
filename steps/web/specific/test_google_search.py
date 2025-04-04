# tests/step_defs/test_google_search.py
from pytest_bdd import scenario, given, when, then
from playwright.sync_api import Page, expect

@scenario('../features/google_search.feature', 'Search for a keyword on Google')
def test_google_search():
    pass

@given('the user is on the Google homepage')
async def google_home(page: Page):
    await page.goto('https://www.google.com')

@when('the user searches for "pytest-bdd"')
async def search_keyword(page: Page):
    await page.fill('input[name="q"]', 'pytest-bdd')
    await page.press('input[name="q"]', 'Enter')

@then('the search results should be displayed')
async def verify_results(page: Page):
    await expect(page).to_have_title(text_pattern="pytest-bdd")