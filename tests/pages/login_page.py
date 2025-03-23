# pages/login_page.py
from pages.base_page import BasePage

class LoginPage(BasePage):
    # Selectors
    USERNAME_INPUT = "#username"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "#login-button"
    ERROR_MESSAGE = ".error-message"
    
    def __init__(self, page, base_url):
        super().__init__(page, base_url)
        self.path = "/login"
    
    def navigate(self):
        """Navigate to login page"""
        return self.navigate_to(self.path)
    
    def login(self, username, password):
        """Perform login with given credentials"""
        self.fill(self.USERNAME_INPUT, username)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
        return self
    
    def get_error_message(self):
        """Get error message text if present"""
        if self.is_visible(self.ERROR_MESSAGE):
            return self.get_element(self.ERROR_MESSAGE).text_content()
        return None
    
    def verify_login_page_visual(self):
        """Verify login page visually"""
        return self.verify_visual("login_page")