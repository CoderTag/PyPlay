# steps/web/specific/login_steps.py

from pytest_bdd import given, when, then, parsers

@given(parsers.parse('the web application is open on the "{page_name}" page'))
async def open_web_page(page_objects, page_name):
    """Open the specified page in the web application."""
    if page_name.lower() == "login":
        await page_objects["login_page"].navigate()
    elif page_name.lower() == "dashboard":
        # Navigate to dashboard page
        await page_objects["base_page"].navigate_to("dashboard")
    else:
        # Generic navigation to any page by name
        await page_objects["base_page"].navigate_to(page_name.lower())

@when(parsers.parse('the user enters "{text}" in the "{field_name}" field'))
async def enter_text_in_field(page_objects, text, field_name):
    """Enter text in the specified field."""
    await page_objects["base_page"].fill(field_name, text)

@when(parsers.parse('the user clicks the "{button_name}" button'))
async def click_button(page_objects, button_name):
    """Click the specified button."""
    await page_objects["base_page"].click_element(button_name)

@when(parsers.parse('the user checks the "{checkbox_name}" checkbox'))
async def check_checkbox(page_objects, checkbox_name):
    """Check the specified checkbox."""
    await page_objects["base_page"].check_checkbox(checkbox_name)

@then(parsers.parse('the user should be redirected to the "{page_name}" page'))
async def verify_page_redirect(page_objects, page_name):
    """Verify that the user is redirected to the specified page."""
    is_current = await page_objects["base_page"].is_current_page(page_name)
    assert is_current, f"Expected to be on {page_name} page but was not"

@then(parsers.parse('the element "{element_name}" should display text "{expected_text}"'))
async def verify_element_text(page_objects, element_name, expected_text):
    """Verify that the specified element displays the expected text."""
    actual_text = await page_objects["base_page"].get_element_text(element_name)
    assert actual_text == expected_text, f"Expected text '{expected_text}' but got '{actual_text}'"

@then(parsers.parse('an error message "{error_message}" should be displayed'))
async def verify_error_message(page_objects, error_message):
    """Verify that the specified error message is displayed."""
    is_displayed = await page_objects["login_page"].is_error_displayed(error_message)
    assert is_displayed, f"Error message '{error_message}' not displayed"

@then(parsers.parse('the user should remain on the "{page_name}" page'))
async def verify_current_page(page_objects, page_name):
    """Verify that the user remains on the specified page."""
    is_current = await page_objects["base_page"].is_current_page(page_name)
    assert is_current, f"Expected to remain on {page_name} page but was not"

@then(parsers.parse('the "{field_name}" field should have type "{input_type}"'))
async def verify_field_type(page_objects, field_name, input_type):
    """Verify the type attribute of the specified field."""
    actual_type = await page_objects["base_page"].get_field_type(field_name)
    assert actual_type == input_type, f"Expected field type '{input_type}' but got '{actual_type}'"