import os
import asyncio
import structlog
from pytest_bdd import given, when, then, parsers
from assertpy import assert_that
from playwright.async_api import async_playwright
import pytest
from pytest_bdd import given, when, then, parsers
from playwright.sync_api import Page


logger = structlog.get_logger(__name__)

# Utility class for Playwright operations
class PlaywrightHelper:
    def __init__(self, page):
        self.page = page

    async def set_window_size(self, width, height):
        logger.info(f"Setting window size: {width}x{height}")
        await self.page.set_viewport_size({"width": width, "height": height})

    async def maximize_window(self):
        logger.info("Maximizing window (setting large viewport size)")
        await self.page.set_viewport_size({"width": 1920, "height": 1080})

    async def navigate_to_url(self, url):
        logger.info(f"Navigating to URL: {url}")
        await self.page.goto(url)

    async def refresh_page(self):
        logger.info("Refreshing page")
        await self.page.reload()

    async def get_current_url(self):
        url = self.page.url
        logger.info(f"Current URL: {url}")
        return url

    async def get_title(self):
        title = await self.page.title()
        logger.info(f"Page title: {title}")
        return title

@given(parsers.re("The browser resolution is '(?P<width>.*)' per '(?P<height>.*)'"))
@when(parsers.re("The browser resolution is '(?P<width>.*)' per '(?P<height>.*)'"))
async def set_browser_resolution(page, width: str, height: str):
    helper = PlaywrightHelper(page)
    await helper.set_window_size(int(width), int(height))

@given("Browser is maximized")
@when("Browser is maximized")
async def maximize_browser(page):
    helper = PlaywrightHelper(page)
    await helper.maximize_window()

@given(parsers.re("I am on the (url|page|site) '(?P<page_url>.*)'"))
@when(parsers.re("I am on the (url|page|site) '(?P<page_url>.*)'"))
async def open_webpage(page, base_url: str, page_url: str):
    helper = PlaywrightHelper(page)
    await helper.navigate_to_url(f"{base_url}{page_url}")

@given(parsers.re("I navigate to external page '(?P<url>.*)'"))
@when(parsers.re("I navigate to external page '(?P<url>.*)'"))
async def navigate_to_external(page, url: str):
    helper = PlaywrightHelper(page)
    await helper.navigate_to_url(url)

@given(parsers.re("I get current browser url and store it to '(?P<env_var>.*)'"))
@then(parsers.re("I get current browser url and store it to '(?P<env_var>.*)'"))
async def store_current_url(page, env_var: str):
    helper = PlaywrightHelper(page)
    os.environ[env_var] = await helper.get_current_url()

@given("I navigate back to the previous page")
@when("I navigate back to the previous page")
async def navigate_back(page):
    logger.info("Navigating back")
    await page.go_back()

@given(parsers.re("The title is '(?P<title>.*)'"))
@then(parsers.re("The title is '(?P<title>.*)'"))
async def check_page_title(page, title: str):
    helper = PlaywrightHelper(page)
    actual_title = await helper.get_title()
    assert_that(actual_title).is_equal_to(title)

@given(parsers.re("The title is not '(?P<title>.*)'"))
@then(parsers.re("The title is not '(?P<title>.*)'"))
async def check_page_title_not(page, title: str):
    helper = PlaywrightHelper(page)
    actual_title = await helper.get_title()
    assert_that(actual_title).is_not_equal_to(title)

@given(parsers.re("I refresh the current page"))
@when(parsers.re("I refresh the current page"))
async def refresh_current_page(page):
    helper = PlaywrightHelper(page)
    await helper.refresh_page()

# Suggested filename: web_common_playwright_steps.py

# Required packages:
# - playwright
# - pytest
# - pytest-bdd
# - assertpy
# - structlog
# - asyncio
# Example utility function (like should_skip_step) placeholder
def should_skip_step(env_var, expected_value):
    # Implement environment checks if needed
    return False

@given(parsers.re("There is just one (browser tab|window) open"))
@when(parsers.re("There is just one (browser tab|window) open"))
def close_all_but_first_tab(page: Page):
    while len(page.context.pages) > 1:
        page.context.pages[-1].close()

@given(parsers.re("I open new tab with url '(?P<page_url>.*)'"))
@when(parsers.re("I open new tab with url '(?P<page_url>.*)'"))
def open_specific_tab(page: Page, page_url):
    page.context.new_page().goto(page_url)

@then(parsers.re("The url '(?P<url>.*)' is opened in a new (tab|window)"))
def check_is_opened_in_new_window(page: Page, url):
    assert page.context.pages[-1].url.startswith(url)

@given(parsers.re("I close the last opened window"))
@when(parsers.re("I close the last opened window"))
def close_last_opened_window(page: Page):
    if len(page.context.pages) > 1:
        page.context.pages[-1].close()

@given(parsers.re("I focus the last opened window"))
@when(parsers.re("I focus the last opened window"))
def switch_to_last(page: Page):
    last_page = page.context.pages[-1]
    last_page.bring_to_front()

@then(parsers.re("There are '(?P<count>.*)' (tabs|windows) currently opened"))
def check_number_of_tabs(page: Page, count: int):
    assert len(page.context.pages) == count

@given(parsers.re("I close the current opened tab"))
@when(parsers.re("I close the current opened tab"))
def close_current_opened_tab(page: Page):
    page.close()

@given(parsers.re("I switch to tab with url '(?P<value>.*)'"))
@when(parsers.re("I switch to tab with url '(?P<value>.*)'"))
def switch_specific_tab(page: Page, value: str):
    for p in page.context.pages:
        if p.url.startswith(value):
            p.bring_to_front()
            break

@given(parsers.re("I close the tab with url '(?P<value>.*)'"))
@when(parsers.re("I close the tab with url '(?P<value>.*)'"))
def close_specific_tab(page: Page, value: str):
    for p in page.context.pages:
        if p.url.startswith(value):
            p.close()
            break

@then(parsers.re("A new (tab|window) is opened"))
def check_new_window(page: Page):
    assert len(page.context.pages) > 1

@then(parsers.re("A new (tab|window) is not opened"))
def check_no_new_window(page: Page):
    assert len(page.context.pages) == 1

@given(parsers.re("I switch to iframe '(?P<selector>.*)'"))
@when(parsers.re("I switch to iframe '(?P<selector>.*)'"))
def switch_to_iframe(page: Page, selector):
    frame = page.frame_locator(selector)
    assert frame

@given(parsers.re("I switch back from iframe"))
@when(parsers.re("I switch back from iframe"))
def switch_back_from_iframe(page: Page):
    page.main_frame()

@given(parsers.re("I take a screenshot"))
@when(parsers.re("I take a screenshot"))
@then(parsers.re("I take a screenshot"))
def take_a_screenshot(page: Page):
    page.screenshot(path="screenshot.png")

@given(parsers.re("I attach file '(?P<file_path>.*)' to input field '(?P<selector>.*)'"))
@when(parsers.re("I attach file '(?P<file_path>.*)' to input field '(?P<selector>.*)'"))
def attach_file(page: Page, file_path, selector):
    page.set_input_files(selector, file_path)

@then(parsers.re("The cookie '(?P<name>.*)' contains the value '(?P<value>.*)'"))
def check_cookie_content(page: Page, name, value):
    cookies = page.context.cookies()
    cookie = next((c for c in cookies if c['name'] == name), None)
    assert cookie and value in cookie['value']

# Utility functions
def should_skip_step(env_var, expected_value):
    if env_var and expected_value:
        return os.getenv(env_var) != expected_value
    return False


def soft_assert(condition, message="Assertion failed"):
    try:
        assert condition, message
    except AssertionError as e:
        print(f"Soft assert failed: {e}")


@given(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?The cookie '(?P<name>.*)' exists(?: if '(?P<env_var>.*)' is set to '(?P<expected_value>.*)' value)?$"))
@when(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?The cookie '(?P<name>.*)' exists(?: if '(?P<env_var>.*)' is set to '(?P<expected_value>.*)' value)?$"))
@then(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?The cookie '(?P<name>.*)' exists(?: if '(?P<env_var>.*)' is set to '(?P<expected_value>.*)' value)?$"))
def check_cookie_exists(page: Page, soft_assert: str, name, env_var, expected_value):
    if should_skip_step(env_var, expected_value):
        return

    cookie = page.context.cookies()
    cookie_names = [c['name'] for c in cookie]

    if soft_assert and soft_assert.lower() == 'true':
        soft_assert(name in cookie_names, f"Cookie '{name}' not found")
    else:
        assert name in cookie_names


@given(parsers.re("I set the cookie '(?P<name>.*)' with value '(?P<value>.*)' for path '(?P<path>.*)'(?: if '(?P<env_var>.*)' is set to '(?P<expected_value>.*)' value)?$"))
@when(parsers.re("I set the cookie '(?P<name>.*)' with value '(?P<value>.*)' for path '(?P<path>.*)'(?: if '(?P<env_var>.*)' is set to '(?P<expected_value>.*)' value)?$"))
def set_cookie(page: Page, name, value, path, env_var, expected_value):
    if should_skip_step(env_var, expected_value):
        return

    page.context.add_cookies([{"name": name, "value": value, "path": path, "url": page.url}])


@given(parsers.re("I delete the cookie '(?P<name>.*)'(?: if '(?P<env_var>.*)' is set to '(?P<expected_value>.*)' value)?$"))
@when(parsers.re("I delete the cookie '(?P<name>.*)'(?: if '(?P<env_var>.*)' is set to '(?P<expected_value>.*)' value)?$"))
def delete_cookie(page: Page, name, env_var, expected_value):
    if should_skip_step(env_var, expected_value):
        return

    cookies = page.context.cookies()
    for c in cookies:
        if c['name'] == name:
            page.context.clear_cookies()


@given(parsers.re("I accept popup (prompt|alertbox|confirmbox)(?: if '(?P<env_var>.*)' is set to '(?P<expected_value>.*)' value)?$"))
@when(parsers.re("I accept popup (prompt|alertbox|confirmbox)(?: if '(?P<env_var>.*)' is set to '(?P<expected_value>.*)' value)?$"))
def accept_alert(page: Page, env_var, expected_value):
    if should_skip_step(env_var, expected_value):
        return

    with page.expect_event("dialog") as dialog_info:
        dialog = dialog_info.value
        dialog.accept()

