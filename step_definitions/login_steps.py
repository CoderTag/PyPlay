# step_definitions/login_steps.py
from pytest_bdd import given, when, then, parsers
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

@given("the user is on the login page")
def user_on_login_page(page, config):
    login_page = LoginPage(page, config["base_url"])
    login_page.navigate()

@when(parsers.parse('the user enters username "{username}"'))
def enter_username(page, config, username):
    login_page = LoginPage(page, config["base_url"])
    # If username is a reference to a user in the config, use that
    if username in config["users"]:
        actual_username = config["users"][username]["username"]
    else:
        actual_username = username
    login_page.fill(login_page.USERNAME_INPUT, actual_username)

@when(parsers.parse('the user enters password "{password}"'))
def enter_password(page, config, password):
    login_page = LoginPage(page, config["base_url"])
    # If password is a reference to a user in the config, use that
    if password in config["users"]:
        actual_password = config["users"][password]["password"]
    else:
        actual_password = password
    login_page.fill(login_page.PASSWORD_INPUT, actual_password)

@when("the user clicks the login button")
def click_login_button(page, config):
    login_page = LoginPage(page, config["base_url"])
    login_page.click(login_page.LOGIN_BUTTON)

@then("the user should be redirected to the dashboard")
def verify_dashboard_redirect(page, config):
    dashboard_page = DashboardPage(page, config["base_url"])
    assert dashboard_page.is_visible(dashboard_page.DASHBOARD_HEADER), "Dashboard not displayed"

@then("an error message should be displayed")
def verify_error_message(page, config):
    login_page = LoginPage(page, config["base_url"])
    assert login_page.is_visible(login_page.ERROR_MESSAGE), "Error message not displayed"

@then("the user should remain on the login page")
def verify_still_on_login_page(page, config):
    login_page = LoginPage(page, config["base_url"])
    assert "/login" in page.url, "User is not on the login page"

@then("the login page should match the baseline")
def verify_login_page_visual(page, config):
    if not config["run_visual"]:
        pytest.skip("Visual testing is disabled")
    
    login_page = LoginPage(page, config["base_url"])
    result = login_page.verify_login_page_visual()
    assert result["status"] in ["match", "baseline_created"], f"Visual verification failed: {result}"