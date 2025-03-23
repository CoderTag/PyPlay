"""
Playwright Step Definitions for Web, Mobile, and API Automation
"""
import re
from typing import Optional, Union
from pytest_bdd import given, when, parsers
from playwright.sync_api import Page, expect, Locator
import logging

logger = logging.getLogger(__name__)

# Configuration constants
class PyPlayConfig:
    BP_SHORT_WAIT_TIMEOUT = 10000  # in milliseconds
    BP_STANDARD_WAIT_TIMEOUT = 30000  # in milliseconds

# Helper functions
def should_skip_step(request, env_var, expected_value):
    """Skip step if environment variable condition is not met"""
    if env_var and expected_value:
        actual_value = request.config.getoption(f"--{env_var}", default=None)
        if actual_value != expected_value:
            request.node.user_properties.append(("skipped_step", True))
            return True
    return False

class FeatureManager:
    @staticmethod
    def use(feature_name, **kwargs):
        """Feature flag management"""
        # This is a placeholder that can be implemented as needed
        pass

class PlaywrightContext:
    def __init__(self, page: Page):
        self.page = page
        self.mobile_context = None

    def __enter__(self):
        """Enter mobile context if needed"""
        # This would be implemented based on your specific mobile testing needs
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit mobile context if needed"""
        # This would be implemented based on your specific mobile testing needs
        pass

class PlaywrightGenerics:
    def __init__(self, page: Page):
        self.page = page
        self.capabilities = {}  # This would be populated with browser info

    def is_android(self):
        """Check if the current platform is Android"""
        return self.capabilities.get('platformName', '').lower() == 'android'
    
    def is_mobile(self):
        """Check if the current platform is mobile"""
        return self.is_android() or (self.capabilities.get('platformName', '').lower() == 'ios')
    
    def get_element(self, selector):
        """Get element by selector"""
        return self.page.locator(selector).first
    
    def get_elements(self, selector):
        """Get elements by selector"""
        return self.page.locator(selector).all()
    
    def click(self, selector, max_wait_time=None):
        """Click on element with wait"""
        wait_time = max_wait_time if max_wait_time else BPConfig.BP_SHORT_WAIT_TIMEOUT
        locator = self.page.locator(selector)
        
        logger.info(f"Clicking on element: {selector}")
        # Wait for the element to be visible and stable
        locator.wait_for(timeout=wait_time)
        locator.click()
    
    def double_click(self, selector):
        """Double click on element"""
        locator = self.page.locator(selector)
        locator.wait_for()
        locator.dblclick()
    
    def click_by_action(self, selector):
        """Click on element using JavaScript"""
        self.page.locator(selector).evaluate("el => el.click()")
    
    def is_element_visible(self, selector, timeout=None):
        """Check if element is visible"""
        wait_time = timeout * 1000 if timeout else BPConfig.BP_SHORT_WAIT_TIMEOUT
        try:
            self.page.locator(selector).wait_for(state="visible", timeout=wait_time)
            return True
        except:
            return False
    
    def press_key(self, key):
        """Press a key"""
        self.page.keyboard.press(key)
    
    def press_key_on_element(self, selector, key):
        """Focus on element and press a key"""
        self.page.locator(selector).focus()
        self.page.keyboard.press(key)
    
    def click_with_percentage(self, page, selector, x_percentage, y_percentage):
        """Click at position calculated as percentage of element size"""
        element = self.page.locator(selector)
        element.wait_for()
        
        # Get element's bounding box
        bbox = element.bounding_box()
        
        # Calculate position
        x = bbox["x"] + (bbox["width"] * int(x_percentage) / 100)
        y = bbox["y"] + (bbox["height"] * int(y_percentage) / 100)
        
        # Click at the calculated position
        self.page.mouse.click(x, y)
    
    def tap_corner_of_element(self, page, corner, selector):
        """Tap on a corner of an element"""
        element = self.page.locator(selector)
        element.wait_for()
        
        # Get element's bounding box
        bbox = element.bounding_box()
        
        # Calculate position based on corner
        if corner == "TOP_LEFT":
            x = bbox["x"] + 5
            y = bbox["y"] + 5
        elif corner == "TOP_RIGHT":
            x = bbox["x"] + bbox["width"] - 5
            y = bbox["y"] + 5
        elif corner == "BOTTOM_LEFT":
            x = bbox["x"] + 5
            y = bbox["y"] + bbox["height"] - 5
        elif corner == "BOTTOM_RIGHT":
            x = bbox["x"] + bbox["width"] - 5
            y = bbox["y"] + bbox["height"] - 5
        
        # Click at the calculated position
        self.page.mouse.click(x, y)
    
    def long_tap(self, page, selector):
        """Long press on element"""
        element = self.page.locator(selector)
        element.wait_for()
        
        # Get element's bounding box for center calculation
        bbox = element.bounding_box()
        x = bbox["x"] + bbox["width"] / 2
        y = bbox["y"] + bbox["height"] / 2
        
        # Long press (700ms)
        self.page.mouse.down(x, y)
        self.page.wait_for_timeout(700)
        self.page.mouse.up(x, y)
    
    def tap_with_percentage(self, page, selector, x_percentage, y_percentage):
        """Tap at position calculated as percentage of element size"""
        # Same implementation as click_with_percentage for mobile
        self.click_with_percentage(page, selector, x_percentage, y_percentage)
    
    def back(self):
        """Go back (for mobile)"""
        self.page.go_back()

class Locators:
    def __init__(self):
        self.MOBILE_SUFFIX = "_mobile"
    
    def parse_and_get(self, locator_path, generics):
        """Parse a locator path and get the appropriate locator"""
        # This is a placeholder that would be implemented based on your locator strategy
        return locator_path
    
    def get_element_by_text(self, value, visibility_option, target_xpath=None):
        """Get element by text with various matching options"""
        base_xpath = target_xpath if target_xpath else "//*"
        
        if visibility_option == "EQUALS":
            return f"{base_xpath}[normalize-space()='{value}']"
        elif visibility_option == "CONTAINS":
            return f"{base_xpath}[contains(normalize-space(),'{value}')]"
        elif visibility_option == "STARTS_WITH":
            return f"{base_xpath}[starts-with(normalize-space(),'{value}')]"
        elif visibility_option == "ENDS_WITH":
            return f"{base_xpath}[substring(normalize-space(), string-length(normalize-space()) - string-length('{value}') + 1) = '{value}']"

# Constants
MOBILE_SUFFIX = "_mobile"

# Set up context manager
def context_manager(driver=None):
    """Context manager for mobile context"""
    return PlaywrightContext(driver.page if driver else None)

# Step definitions
@given(parsers.re("I click on (checkbox|button|dropdown|item|element) '(?P<locator_path>.*)'(?: if '(?P<env_var>.*)' is set to '(?P<expected_value>.*)' value)?$"))
@given(parsers.re("I tap on '(?P<locator_path>.*)'(?: if '(?P<env_var>.*)' is set to '(?P<expected_value>.*)' value)?$"))
@when(parsers.re("I click on (checkbox|button|dropdown|item|element) '(?P<locator_path>.*)'(?: if '(?P<env_var>.*)' is set to '(?P<expected_value>.*)' value)?$"))
@when(parsers.re("I tap on '(?P<locator_path>.*)'(?: if '(?P<env_var>.*)' is set to '(?P<expected_value>.*)' value)?$"))
def click_on_locator(request, page, locators, locator_path, env_var=None, expected_value=None):
    """
    Click on an element identified by the given locator path
    """
    if should_skip_step(request, env_var, expected_value):
        return
    
    playwright_generics = PlaywrightGenerics(page)
    
    if MOBILE_SUFFIX in locator_path:
        with context_manager(playwright_generics):
            page.locator(locators.parse_and_get(locator_path, playwright_generics)).click()
    else:
        page.locator(locators.parse_and_get(locator_path, playwright_generics)).click()

@given(parsers.re(
    "(I wait for maximum '(?P<wait_seconds>\\d+)' seconds, and )?I click on '(?P<locator_path>.+)'(?: if '(?P<env_var>.*)' is set to '(?P<expected_value>.*)' value)?$"))
@when(parsers.re(
    "(I wait for maximum '(?P<wait_seconds>\\d+)' seconds, and )?I click on '(?P<locator_path>.+)'(?: if '(?P<env_var>.*)' is set to '(?P<expected_value>.*)' value)?$"))
def click_element(request, page, locators, locator_path, wait_seconds=None, env_var=None, expected_value=None):
    """
    Click on an element with configurable wait time
    """
    if should_skip_step(request, env_var, expected_value):
        return
    
    playwright_generics = PlaywrightGenerics(page)
    wait_time = int(wait_seconds) * 1000 if wait_seconds else BPConfig.BP_SHORT_WAIT_TIMEOUT
    
    # Playwright's built-in waiting and auto-retry mechanism
    locator = page.locator(locators.parse_and_get(locator_path, playwright_generics))
    locator.wait_for(timeout=wait_time)
    locator.click()

@given(parsers.re("I (double click|doubleclick) on '(?P<locator_path>.*)'(?: if '(?P<env_var>.*)' is set to '(?P<expected_value>.*)' value)?$"))
@when(parsers.re("I (double click|doubleclick) on '(?P<locator_path>.*)'(?: if '(?P<env_var>.*)' is set to '(?P<expected_value>.*)' value)?$"))
def dbl_click_element(request, page, locators, locator_path, env_var=None, expected_value=None):
    """
    Double click on an element
    """
    if should_skip_step(request, env_var, expected_value):
        return
    
    playwright_generics = PlaywrightGenerics(page)
    locator = page.locator(locators.parse_and_get(locator_path, playwright_generics))
    locator.dblclick()

@given(parsers.re("I click on SVG element '(?P<locator_path>.*)'(?: if '(?P<env_var>.*)' is set to '(?P<expected_value>.*)' value)?$"))
@when(parsers.re("I click on SVG element '(?P<locator_path>.*)'(?: if '(?P<env_var>.*)' is set to '(?P<expected_value>.*)' value)?$"))
def click_svg_element(request, page, locators, locator_path, env_var=None, expected_value=None):
    """
    Click on an SVG element using JavaScript
    """
    if should_skip_step(request, env_var, expected_value):
        return
    
    playwright_generics = PlaywrightGenerics(page)
    locator = page.locator(locators.parse_and_get(locator_path, playwright_generics))
    # Use JavaScript click for SVG elements
    locator.evaluate("el => el.click()")

@given(parsers.re("I click on type:'(?P<element_type>.*)' element with text equal to '(?P<value>.*)'(?: if '(?P<env_var>.*)' is set to '(?P<expected_value>.*)' value)?$"))
@when(parsers.re("I click on type:'(?P<element_type>.*)' element with text equal to '(?P<value>.*)'(?: if '(?P<env_var>.*)' is set to '(?P<expected_value>.*)' value)?$"))
def click_on_text(request, page, element_type, value, env_var=None, expected_value=None):
    """
    Click on an element of a specific type with exact text
    """
    if should_skip_step(request, env_var, expected_value):
        return
    
    # Playwright's built-in text selector
    page.locator(f"{element_type}:text-is('{value}')").click()

@given(parsers.re("I click on type:'(?P<element_type>.*)' that contains the text:'(?P<value>.*)'(?: if '(?P<env_var>.*)' is set to '(?P<expected_value>.*)' value)?$"))
@when(parsers.re("I click on type:'(?P<element_type>.*)' that contains the text:'(?P<value>.*)'(?: if '(?P<env_var>.*)' is set to '(?P<expected_value>.*)' value)?$"))
def click_on_partial_text(request, page, element_type, value, env_var=None, expected_value=None):
    """
    Click on an element of a specific type that contains the given text
    """
    if should_skip_step(request, env_var, expected_value):
        return
    
    # Playwright's built-in text selector
    page.locator(f"{element_type}:text('{value}')").click()

@given(parsers.re(r"I click on element with visible text '(?P<visibility_option>EQUALS|CONTAINS|STARTS_WITH|ENDS_WITH)' '(?P<value>.*)'(\s+)?((?:and)\s+(?:')(?P<target_path>.*)(?:') target element)?(?: if '(?P<env_var>.*)' is set to '(?P<expected_value>.*)' value)?$"))
@when(parsers.re(r"I click on element with visible text '(?P<visibility_option>EQUALS|CONTAINS|STARTS_WITH|ENDS_WITH)' '(?P<value>.*)'(\s+)?((?:and)\s+(?:')(?P<target_path>.*)(?:') target element)?(?: if '(?P<env_var>.*)' is set to '(?P<expected_value>.*)' value)?$"))
def click_on_element_by_visible_text(request, page, locators, visibility_option, value, target_path=None, env_var=None, expected_value=None):
    """
    Click on an element by visible text with various matching options
    """
    if should_skip_step(request, env_var, expected_value):
        return
    
    playwright_generics = PlaywrightGenerics(page)
    
    # Parse target path if provided
    parsed_target_path = ""
    if target_path:
        parsed_target_path = locators.parse_and_get(target_path, playwright_generics)
    
    # Convert visibility option to Playwright selector
    if visibility_option == "EQUALS":
        if target_path:
            selector = f"{parsed_target_path} >> text='{value}'"
        else:
            selector = f"text='{value}'"
    elif visibility_option == "CONTAINS":
        if target_path:
            selector = f"{parsed_target_path} >> text='{value}'"
        else:
            selector = f"text='{value}'"
    elif visibility_option == "STARTS_WITH":
        if target_path:
            selector = f"{parsed_target_path} >> text='^{value}'"
        else:
            selector = f"text=^{value}"
    elif visibility_option == "ENDS_WITH":
        if target_path:
            selector = f"{parsed_target_path} >> text='{value}$'"
        else:
            selector = f"text='{value}$'"
    
    # Check if the element is uniquely identified
    elements = page.locator(selector).all()
    if len(elements) == 1:
        page.locator(selector).click()
    else:
        raise Exception(f"Element cannot be uniquely identified. Found: {len(elements)} elements")

@given(parsers.re("I long tap on element '(?P<locator>.*)'(?: if '(?P<env_var>.*)' is set to '(?P<expected_value>.*)' value)?$"))
@when(parsers.re("I long tap on element '(?P<locator>.*)'(?: if '(?P<env_var>.*)' is set to '(?P<expected_value>.*)' value)?$"))
def long_tap(request, page, locators, locator, env_var=None, expected_value=None):
    """
    Long tap on an element (mobile-specific)
    """
    if should_skip_step(request, env_var, expected_value):
        return
    
    playwright_generics = PlaywrightGenerics(page)
    with context_manager(playwright_generics):
        element = page.locator(locators.parse_and_get(locator, playwright_generics))
        # Get element's bounding box for center calculation
        bbox = element.bounding_box()
        x = bbox["x"] + bbox["width"] / 2
        y = bbox["y"] + bbox["height"] / 2
        
        # Long press (700ms)
        page.mouse.down(x, y)
        page.wait_for_timeout(700)
        page.mouse.up(x, y)

@given(parsers.re("I tap '(?P<corner>BOTTOM_LEFT|BOTTOM_RIGHT|TOP_LEFT|TOP_RIGHT)' corner of element '(?P<locator_path>.*)'(?: if '(?P<env_var>.*)' is set to '(?P<expected_value>.*)' value)?$"))
@when(parsers.re("I tap '(?P<corner>BOTTOM_LEFT|BOTTOM_RIGHT|TOP_LEFT|TOP_RIGHT)' corner of element '(?P<locator_path>.*)'(?: if '(?P<env_var>.*)' is set to '(?P<expected_value>.*)' value)?$"))
def click_element_corner(request, page, locators, corner, locator_path, env_var=None, expected_value=None):
    """
    Tap a specific corner of an element
    """
    if should_skip_step(request, env_var, expected_value):
        return
    
    playwright_generics = PlaywrightGenerics(page)
    locator = locators.parse_and_get(locator_path, playwright_generics)
    
    if MOBILE_SUFFIX in locator_path:
        with context_manager(playwright_generics):
            playwright_generics.tap_corner_of_element(playwright_generics, corner, locator)
    else:
        playwright_generics.tap_corner_of_element(playwright_generics, corner, locator)

@given(parsers.re("On '(?P<platform>Android|iOS)' I tap on the x='(?P<x_value>.*)' % and y='(?P<y_value>.*)' % of element '(?P<locator_path>.*)'(?: if '(?P<env_var>.*)' is set to '(?P<expected_value>.*)' value)?$"))
@when(parsers.re("On '(?P<platform>Android|iOS)' I tap on the x='(?P<x_value>.*)' % and y='(?P<y_value>.*)' % of element '(?P<locator_path>.*)'(?: if '(?P<env_var>.*)' is set to '(?P<expected_value>.*)' value)?$"))
def tap_with_percentage(request, page, locators, platform, x_value, y_value, locator_path, env_var=None, expected_value=None):
    """
    Tap on a specific percentage position of an element on mobile devices
    """
    if should_skip_step(request, env_var, expected_value):
        return
    
    playwright_generics = PlaywrightGenerics(page)
    
    # Check if current platform matches the specified platform
    if playwright_generics.capabilities.get('platformName', '').lower() == platform.lower():
        if MOBILE_SUFFIX in locator_path:
            with context_manager(playwright_generics):
                locator = locators.parse_and_get(locator_path, playwright_generics)
                playwright_generics.tap_with_percentage(playwright_generics, locator, x_value, y_value)

@given(parsers.re("On android, I tap on back navigation(?: if '(?P<env_var>.*)' is set to '(?P<expected_value>.*)' value)?$"))
@when(parsers.re("On android, I tap on back navigation(?: if '(?P<env_var>.*)' is set to '(?P<expected_value>.*)' value)?$"))
def tap_back_nav(request, page, env_var=None, expected_value=None):
    """
    Tap on the back navigation button on Android devices
    """
    if should_skip_step(request, env_var, expected_value):
        return
    
    playwright_generics = PlaywrightGenerics(page)
    if playwright_generics.is_android():
        with context_manager(playwright_generics):
            page.go_back()

@given(parsers.re("On iOS, I navigate back to app after clicking on '(?P<locator>.*)'(?: if '(?P<env_var>.*)' is set to '(?P<expected_value>.*)' value)?$"))
@when(parsers.re("On iOS, I navigate back to app after clicking on '(?P<locator>.*)'(?: if '(?P<env_var>.*)' is set to '(?P<expected_value>.*)' value)?$"))
def navigate_back_to_app(request, page, locators, locator, env_var=None, expected_value=None):
    """
    Navigate back to app after clicking on an element on iOS devices
    """
    if should_skip_step(request, env_var, expected_value):
        return
    
    playwright_generics = PlaywrightGenerics(page)
    if not playwright_generics.is_android():
        with context_manager(playwright_generics):
            page.locator(locators.parse_and_get(locator, playwright_generics)).click()

@given(parsers.re("I press '(?P<key>.*)'(?: if '(?P<env_var>.*)' is set to '(?P<expected_value>.*)' value)?$"))
@when(parsers.re("I press '(?P<key>.*)'(?: if '(?P<env_var>.*)' is set to '(?P<expected_value>.*)' value)?$"))
def press_key_not_focused_on_element(request, page, key, env_var=None, expected_value=None):
    """
    Press a keyboard key without focusing on any element
    """
    if should_skip_step(request, env_var, expected_value):
        return
    
    playwright_generics = PlaywrightGenerics(page)
    if playwright_generics.is_mobile() and not playwright_generics.is_android():
        request.node.user_properties.append(("skipped_step", True))
        return
    
    logger.info(f"Pressing Key: {key}")
    page.keyboard.press(key)

@given(parsers.re("I focus over '(?P<locator_path>.*)' then I press '(?P<key>.*)'(?: if '(?P<env_var>.*)' is set to '(?P<expected_value>.*)' value)?$"))
@when(parsers.re("I focus over '(?P<locator_path>.*)' then I press '(?P<key>.*)'(?: if '(?P<env_var>.*)' is set to '(?P<expected_value>.*)' value)?$"))
def press_key_on_element(request, page, locators, locator_path, key, env_var=None, expected_value=None):
    """
    Focus on an element and press a keyboard key
    """
    if should_skip_step(request, env_var, expected_value):
        return
    
    playwright_generics = PlaywrightGenerics(page)
    if playwright_generics.is_mobile() and not playwright_generics.is_android():
        request.node.user_properties.append(("skipped_step", True))
        return
    
    locator = locators.parse_and_get(locator_path, playwright_generics)
    logger.info(f"Pressing Key: {key} on element: {locator}")
    
    # Focus on element first
    page.locator(locator).focus()
    # Then press the key
    page.keyboard.press(key)

@when(parsers.re("I click item '(?P<inner_text>.*)' for element '(?P<locator_path>.*)'(?: if '(?P<env_var>.*)' is set to '(?P<expected_value>.*)' value)?$"))
def add_item_for_element(request, page, locators, inner_text, locator_path, env_var=None, expected_value=None):
    """
    Click on an item with specific inner text within an element
    """
    if should_skip_step(request, env_var, expected_value):
        return
    
    playwright_generics = PlaywrightGenerics(page)
    locator = locators.parse_and_get(locator_path, playwright_generics)
    locator = locator.format(inner_text)
    page.locator(locator).click()

@given(parsers.re("I click on the x='(?P<x_offset>.*)' % and y='(?P<y_offset>.*)' % of element '(?P<locator_path>.*)'"))
@when(parsers.re("I click on the x='(?P<x_offset>.*)' % and y='(?P<y_offset>.*)' % of element '(?P<locator_path>.*)'"))
def click_with_percentage(page, locators, x_offset, y_offset, locator_path):
    """
    Click on a specific percentage position of an element
    """
    playwright_generics = PlaywrightGenerics(page)
    locator = locators.parse_and_get(locator_path, playwright_generics)
    
    # Get element's bounding box
    element = page.locator(locator)
    bbox = element.bounding_box()
    
    # Calculate position
    x = bbox["x"] + (bbox["width"] * int(x_offset) / 100)
    y = bbox["y"] + (bbox["height"] * int(y_offset) / 100)
    
    # Click at calculated position
    page.mouse.click(x, y)

@given(parsers.re("(If element is visible within '(?P<timeout>.*)' seconds )?I click on '(?P<locator_path>.*)' and dismiss a popup(?: if '(?P<env_var>.*)' is set to '(?P<expected_value>.*)' value)?$"))
@when(parsers.re("(If element is visible within '(?P<timeout>.*)' seconds )?I click on '(?P<locator_path>.*)' and dismiss a popup(?: if '(?P<env_var>.*)' is set to '(?P<expected_value>.*)' value)?$"))
def dismiss_popup(request, page, locators, locator_path, timeout=None, env_var=None, expected_value=None):
    """
    Click on an element to dismiss a popup if it's visible
    """
    if should_skip_step(request, env_var, expected_value):
        return
    
    playwright_generics = PlaywrightGenerics(page)
    timeout_ms = int(timeout) * 1000 if timeout else 10000
    locator = locators.parse_and_get(locator_path, playwright_generics)
    
    # Check if element is visible
    try:
        element = page.locator(locator)
        element.wait_for(state="visible", timeout=timeout_ms)
        element.click()
    except:
        # Element not visible within timeout
        pass