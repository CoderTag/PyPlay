# pages/base_page.py
from playwright.sync_api import Page, expect

class BasePage:
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url
    
    def navigate_to(self, path=""):
        """Navigate to a specific path from base URL"""
        full_url = f"{self.base_url}{path}"
        self.page.goto(full_url)
        return self
    
    def get_element(self, selector):
        """Get an element with explicit waiting"""
        self.page.wait_for_selector(selector, state="visible")
        return self.page.locator(selector)
    
    def click(self, selector):
        """Click an element after ensuring it's visible"""
        self.get_element(selector).click()
        return self
    
    def fill(self, selector, text):
        """Fill a form field"""
        self.get_element(selector).fill(text)
        return self
    
    def is_visible(self, selector):
        """Check if element is visible"""
        return self.page.locator(selector).is_visible()
    
    def take_screenshot(self, name="screenshot"):
        """Take a screenshot"""
        self.page.screenshot(path=f"screenshots/{name}.png")
        return self
    
    def verify_visual(self, name, selector=None):
        """Perform visual verification using Testim"""
        from utils.visual_testing import compare_visual
        
        if selector:
            element = self.get_element(selector)
            screenshot = element.screenshot()
        else:
            screenshot = self.page.screenshot()
        
        return compare_visual(screenshot, name)