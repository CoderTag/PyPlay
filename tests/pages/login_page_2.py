# pages/login_page_2.py
# Its the same login page but support accssing selectors using configuration approach
# that is selectors are in json or yaml file. Not in a class file. 
from pages.base_page import BasePage
from utils.selector_loader import SelectorLoader

class LoginPage(BasePage):
    def __init__(self, page, base_url):
        super().__init__(page, base_url)
        self.path = "/login"
        self.selectors = SelectorLoader().get_selectors("login_page")
    
    async def navigate(self):
        """Navigate to login page"""
        try:
            return await self.navigate_to(self.path)
        except Exception as e:
            self.logger.error(f"Failed to navigate to login page: {str(e)}")
            raise
    
    async def login(self, username, password):
        """Perform login with given credentials"""
        try:
            # Using get() with default values provides fallback if config is incomplete
            username_selector = self.selectors.get("username_input", "#username")
            password_selector = self.selectors.get("password_input", "#password")
            login_button_selector = self.selectors.get("login_button", "#login-button")
            
            await self.fill(username_selector, username)
            await self.fill(password_selector, password)
            await self.click(login_button_selector)
            await self.wait_for_navigation()
            return self
        except Exception as e:
            self.logger.error(f"Login failed: {str(e)}")
            raise
    
    # Rest of the methods...