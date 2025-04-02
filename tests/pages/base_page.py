# pages/base_page.py
from playwright.async_api import Page, expect
import logging
import asyncio
from typing import Optional, Union

class BasePage:
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url
        self.logger = logging.getLogger(__name__)
        
    async def navigate_to(self, path=""):
        """Navigate to a specific path from base URL"""
        try:
            full_url = f"{self.base_url}{path}"
            self.logger.info(f"Navigating to: {full_url}")
            response = await self.page.goto(full_url, wait_until="networkidle")
            
            if response and not response.ok:
                self.logger.error(f"Navigation failed with status: {response.status}")
                raise Exception(f"Navigation failed with status: {response.status}")
                
            return self
        except Exception as e:
            self.logger.error(f"Navigation error: {str(e)}")
            raise
    
    async def get_element(self, selector, timeout=30000):
        """Get an element with explicit waiting"""
        try:
            self.logger.debug(f"Waiting for selector: {selector}")
            await self.page.wait_for_selector(selector, state="visible", timeout=timeout)
            return self.page.locator(selector)
        except Exception as e:
            self.logger.error(f"Element not found: {selector}. Error: {str(e)}")
            raise
    
    async def click(self, selector, timeout=30000):
        """Click an element after ensuring it's visible"""
        try:
            element = await self.get_element(selector, timeout)
            self.logger.debug(f"Clicking on element: {selector}")
            await element.click()
            return self
        except Exception as e:
            self.logger.error(f"Failed to click element: {selector}. Error: {str(e)}")
            raise
    
    async def fill(self, selector, text, timeout=30000):
        """Fill a form field"""
        try:
            element = await self.get_element(selector, timeout)
            self.logger.debug(f"Filling text in element: {selector}")
            await element.fill(text)
            return self
        except Exception as e:
            self.logger.error(f"Failed to fill element: {selector}. Error: {str(e)}")
            raise
    
    async def is_visible(self, selector, timeout=5000):
        """Check if element is visible"""
        try:
            await self.page.wait_for_selector(selector, state="visible", timeout=timeout)
            return True
        except:
            return False
    
    async def take_screenshot(self, name="screenshot", path="screenshots"):
        """Take a screenshot"""
        try:
            import os
            os.makedirs(path, exist_ok=True)
            self.logger.info(f"Taking screenshot: {name}")
            await self.page.screenshot(path=f"{path}/{name}.png")
            return self
        except Exception as e:
            self.logger.error(f"Failed to take screenshot: {str(e)}")
            raise
    
    async def verify_visual(self, name, selector=None):
        """Perform visual verification using Testim"""
        try:
            from utils.visual_testing import compare_visual
            
            screenshot = None
            if selector:
                element = await self.get_element(selector)
                screenshot = await element.screenshot()
            else:
                screenshot = await self.page.screenshot()
            
            return await compare_visual(screenshot, name)
        except Exception as e:
            self.logger.error(f"Visual verification failed: {str(e)}")
            raise
    
    async def wait_for_navigation(self, timeout=30000):
        """Wait for navigation to complete"""
        try:
            self.logger.debug("Waiting for navigation to complete")
            await self.page.wait_for_load_state("networkidle", timeout=timeout)
            return self
        except Exception as e:
            self.logger.error(f"Navigation timeout: {str(e)}")
            raise
    
    async def get_text(self, selector, timeout=30000):
        """Get text content of an element"""
        try:
            element = await self.get_element(selector, timeout)
            text = await element.text_content()
            return text
        except Exception as e:
            self.logger.error(f"Failed to get text from {selector}: {str(e)}")
            raise
    
    async def select_option(self, selector, value=None, label=None, index=None, timeout=30000):
        """Select an option from a dropdown"""
        try:
            element = await self.get_element(selector, timeout)
            if value:
                await element.select_option(value=value)
            elif label:
                await element.select_option(label=label)
            elif index is not None:
                await element.select_option(index=index)
            return self
        except Exception as e:
            self.logger.error(f"Failed to select option on {selector}: {str(e)}")
            raise
            
    async def hover(self, selector, timeout=30000):
        """Hover over an element"""
        try:
            element = await self.get_element(selector, timeout)
            await element.hover()
            return self
        except Exception as e:
            self.logger.error(f"Failed to hover over {selector}: {str(e)}")
            raise