# pages/login_page.py
from pages.base_page import BasePage
from selectors.login_selectors import LoginSelectors

class LoginPage(BasePage):
    def __init__(self, page, base_url):
        super().__init__(page, base_url)
        self.path = "/login"
        self.selectors = LoginSelectors()
    
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
            await self.fill(self.selectors.USERNAME_INPUT, username)
            await self.fill(self.selectors.PASSWORD_INPUT, password)
            await self.click(self.selectors.LOGIN_BUTTON)
            # Wait for navigation after login
            await self.wait_for_navigation()
            return self
        except Exception as e:
            self.logger.error(f"Login failed: {str(e)}")
            raise
    
    async def get_error_message(self):
        """Get error message text if present"""
        try:
            if await self.is_visible(self.selectors.ERROR_MESSAGE):
                element = await self.get_element(self.selectors.ERROR_MESSAGE)
                return await element.text_content()
            return None
        except Exception as e:
            self.logger.error(f"Failed to get error message: {str(e)}")
            return None
    
    async def verify_login_page_visual(self):
        """Verify login page visually"""
        try:
            return await self.verify_visual("login_page")
        except Exception as e:
            self.logger.error(f"Visual verification failed: {str(e)}")
            raise
    
    async def is_logged_in(self):
        """Check if user is logged in successfully"""
        try:
            # Assuming there's a dashboard element or something that appears after login
            return await self.is_visible(self.selectors.LOGGED_IN_INDICATOR, timeout=5000)
        except Exception as e:
            self.logger.debug(f"User appears to not be logged in: {str(e)}")
            return False