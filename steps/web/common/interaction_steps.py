# steps/web/common/interaction_steps.py
from pytest_bdd import when, parsers
# Assuming BasePage is accessible, e.g., via another fixture or direct import
from targets.web.pages.base_page import BasePage

# Use parsers.re which is powerful for capturing named groups including the complex key
@when(parsers.re(r'the user clicks the "(?P<selector_key>\{.*?\s*>\s*.*?\})".*'))
def click_element_step(browser, selector_key, resolve_selector): # Inject resolve_selector fixture
    """Clicks an element identified by its {file > key}."""
    locator_tuple = resolve_selector(selector_key) # Get (type, value)
    page = BasePage(browser) # Instantiate or get BasePage
    page.click_element(locator_tuple)

@when(parsers.re(r'the user enters "(?P<text_to_enter>.*?)" in the "(?P<selector_key>\{.*?\s*>\s*.*?\})" field'))
def enter_text_step(browser, text_to_enter, selector_key, resolve_selector):
    """Enters text into a field identified by its {file > key}."""
    locator_tuple = resolve_selector(selector_key)
    page = BasePage(browser)
    page.enter_text(locator_tuple, text_to_enter)

@when(parsers.re(r'the user checks the "(?P<selector_key>\{.*?\s*>\s*.*?\})" checkbox'))
def check_checkbox_step(browser, selector_key, resolve_selector):
    """Checks a checkbox identified by its {file > key}."""
    locator_tuple = resolve_selector(selector_key)
    page = BasePage(browser)
    page.check_checkbox(locator_tuple) # Assumes BasePage has this helper

# --- Adapt Assertion Steps Similarly ---
# steps/web/common/assertion_steps.py
from pytest_bdd import then, parsers
from targets.web.pages.base_page import BasePage

@then(parsers.re(r'the element "(?P<selector_key>\{.*?\s*>\s*.*?\})" should display text "(?P<expected_text>.*?)"'))
def verify_element_text(browser, selector_key, expected_text, resolve_selector):
    """Verifies the text content of an element identified by {file > key}."""
    locator_tuple = resolve_selector(selector_key)
    page = BasePage(browser)
    actual_text = page.get_element_text(locator_tuple)
    assert actual_text == expected_text, f"Expected text '{expected_text}' but found '{actual_text}' for element {selector_key}"

@then(parsers.re(r'an error message "(?P<selector_key>\{.*?\s*>\s*.*?\})" should be displayed'))
def verify_error_displayed(browser, selector_key, resolve_selector):
     """Checks if an error message element identified by {file > key} is visible."""
     locator_tuple = resolve_selector(selector_key)
     page = BasePage(browser)
     assert page.is_element_visible(locator_tuple), f"Error message element {selector_key} was not visible."


@then(parsers.re(r'the "(?P<selector_key>\{.*?\s*>\s*.*?\})" field should have attribute "(?P<attribute_name>.*?)" with value "(?P<expected_value>.*?)"'))
def verify_element_attribute(browser, selector_key, attribute_name, expected_value, resolve_selector):
    """Verifies the value of a specific attribute for an element."""
    locator_tuple = resolve_selector(selector_key)
    page = BasePage(browser)
    actual_value = page.get_element_attribute(locator_tuple, attribute_name)
    assert actual_value == expected_value, f"Expected attribute '{attribute_name}' to be '{expected_value}' but found '{actual_value}' for element {selector_key}"