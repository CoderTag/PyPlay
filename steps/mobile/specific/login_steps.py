# steps/mobile/specific/login_steps.py

from pytest_bdd import given, when, then, parsers
from targets.mobile.screens.login_screen import LoginScreen
from targets.mobile.screens.base_screen import BaseScreen
from targets.mobile.helpers.gestures import Gestures

@given(parsers.parse('the mobile app "{app_name}" is installed and launched'))
def launch_mobile_app(app_driver, app_name):
    """Launch the specified mobile app."""
    base_screen = BaseScreen(app_driver)
    base_screen.verify_app_launched(app_name)

@given(parsers.parse('the user is on the "{screen_name}" screen'))
def verify_current_screen(app_driver, screen_name):
    """Verify that the user is on the specified screen."""
    base_screen = BaseScreen(app_driver)
    assert base_screen.is_current_screen(screen_name), f"Expected to be on {screen_name} screen but was not"

@given(parsers.parse('the device has "{connection_status}" connection'))
def set_device_connection(app_driver, connection_status):
    """Set the device's connection status."""
    # Implementation depends on how you control network state in your tests
    if connection_status.lower() == "no internet":
        app_driver.set_network_connection(0)  # Airplane mode in Appium
    elif connection_status.lower() == "wifi":
        app_driver.set_network_connection(2)  # Wifi only
    # Add more conditions as needed

@when(parsers.parse('the user enters "{text}" in the "{field_name}" field'))
def enter_text_in_mobile_field(app_driver, text, field_name):
    """Enter text in the specified mobile field."""
    base_screen = BaseScreen(app_driver)
    base_screen.enter_text(field_name, text)

@when(parsers.parse('the user taps the "{button_name}" button'))
def tap_button(app_driver, button_name):
    """Tap the specified button."""
    base_screen = BaseScreen(app_driver)
    base_screen.tap_element(button_name)

@when(parsers.parse('the system "{dialog_name}" dialog appears'))
def verify_system_dialog(app_driver, dialog_name):
    """Verify that the specified system dialog appears."""
    base_screen = BaseScreen(app_driver)
    assert base_screen.is_dialog_visible(dialog_name), f"Expected {dialog_name} dialog did not appear"

@when(parsers.parse('the user authenticates with "{auth_method}"'))
def authenticate_with_method(app_driver, auth_method):
    """Authenticate using the specified method."""
    if auth_method.lower() == "face id":
        # Mock Face ID authentication for iOS
        app_driver.execute_script('mobile: biometric', {'type': 'faceId', 'state': 'matched'})
    elif auth_method.lower() == "fingerprint":
        # Mock fingerprint authentication for Android
        app_driver.fingerprint(1)  # 1 is success in Android emulator

@when(parsers.parse('the app is in "{app_state}" for "{time_period}"'))
def set_app_state(app_driver, app_state, time_period):
    """Set the app to the specified state for the specified time period."""
    import time
    from datetime import datetime, timedelta
    
    # Parse time period (e.g., "30 minutes" to seconds)
    value, unit = time_period.split()
    seconds = 0
    if unit.lower().startswith('min'):
        seconds = int(value) * 60
    elif unit.lower().startswith('sec'):
        seconds = int(value)
    
    # Set app state
    if app_state.lower() == "background":
        app_driver.background_app(seconds)
    # Add more states as needed

@then(parsers.parse('the user should be navigated to the "{screen_name}" screen'))
def verify_screen_navigation(app_driver, screen_name):
    """Verify that the user is navigated to the specified screen."""
    base_screen = BaseScreen(app_driver)
    assert base_screen.is_current_screen(screen_name), f"Expected to navigate to {screen_name} screen but did not"

@then(parsers.parse('the "{element_name}" should be visible'))
def verify_element_visible(app_driver, element_name):
    """Verify that the specified element is visible."""
    base_screen = BaseScreen(app_driver)
    assert base_screen.is_element_visible(element_name), f"Element {element_name} is not visible"

@then(parsers.parse('an error toast message "{error_message}" should be displayed'))
def verify_toast_message(app_driver, error_message):
    """Verify that the specified toast message is displayed."""
    base_screen = BaseScreen(app_driver)
    assert base_screen.is_toast_visible(error_message), f"Toast message '{error_message}' not displayed"

@then(parsers.parse('an option to "{action_name}" should be available'))
def verify_action_available(app_driver, action_name):
    """Verify that the specified action is available."""
    base_screen = BaseScreen(app_driver)
    assert base_screen.is_action_available(action_name), f"Action {action_name} is not available"