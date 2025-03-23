from pytest_bdd import scenarios, given, when, then, parsers
from locators import Locators
from pages.base_page import BasePage
import pytest
import os
from playwright.async_api import async_playwright

scenarios('../features/google_search.feature')

@pytest.fixture
async def browser():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        yield browser
        await browser.close()

@pytest.fixture
async def page(browser):
    context = await browser.new_context()
    page = await context.new_page()
    yield page
    await context.close()

@pytest.fixture
async def base_page(page):
    return BasePage(page)

@given(parsers.re(r"The browser resolution is '(?P<width>.*)' per '(?P<height>.*)'"))
async def set_browser_resolution(page, width, height):
    await page.set_viewport_size({"width": int(width), "height": int(height)})

@given(parsers.re(r"I am on the (url|page|site) '(?P<page_url>.*)'(?: if '(?P<env_var>.*)' is set to '(?P<expected_value>.*)' value)?$"))
async def navigate_to_page(base_page, page_url, env_var=None, expected_value=None):
    if env_var and expected_value:
        if os.getenv(env_var) == expected_value:
            await base_page.navigate(page_url)
    else:
        await base_page.navigate(page_url)

@when(parsers.re(r"I click on the element with locator '(?P<locator>.*)'"))
async def click_element(base_page, locator):
    await base_page.click(locator)

@when(parsers.re(r"I fill the element with locator '(?P<locator>.*)' with text '(?P<text>.*)'"))
async def fill_element(base_page, locator, text):
    await base_page.fill(locator, text)

@when(parsers.re(r"I press '(?P<key>.*)' on the element with locator '(?P<locator>.*)'"))
async def press_key(base_page, locator, key):
    await base_page.press(locator, key)

@then(parsers.re(r"The element with locator '(?P<locator>.*)' should be visible"))
async def element_should_be_visible(base_page, locator):
    assert await base_page.wait_for_selector(locator)

@then(parsers.re(r"The page URL should contain '(?P<text>.*)'"))
async def url_should_contain(base_page, text):
    assert await base_page.url_contains(text)