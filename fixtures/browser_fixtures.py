# fixtures/web_fixtures.py

import pytest
import configparser
from playwright.async_api import async_playwright
from targets.web.pages.base_page import BasePage
from targets.web.pages.login_page import LoginPage
import yaml
import os
import logging

def load_config(env='dev', platform='web'):
    """Load configuration for the specified environment and platform."""
    config_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config')
    
    # Load common config
    with open(os.path.join(config_dir, 'common_config.yaml'), 'r') as file:
        common_config = yaml.safe_load(file) or {}
    
    # Load platform-specific config
    with open(os.path.join(config_dir, 'platforms', f'{platform}_config.yaml'), 'r') as file:
        platform_config = yaml.safe_load(file) or {}
    
    # Load environment-specific config
    with open(os.path.join(config_dir, 'environments', f'{env}.yaml'), 'r') as file:
        env_config = yaml.safe_load(file) or {}
    
    # Merge configs with environment-specific taking precedence
    # First merge common and web configs
    config = {**common_config, **platform_config}
    
    # Then override with environment-specific web config
    if 'web' in env_config:
        # For web-specific settings in env file
        if 'web' in config:
            config['web'] = {**config['web'], **env_config['web']}
        else:
            config['web'] = env_config['web']
    
    # Add other environment settings
    for key, value in env_config.items():
        if key != 'web':  # Skip web as we've already handled it
            config[key] = value

    return config

@pytest.fixture(scope="session")
def config(request):
    """Fixture to load and provide configuration."""

    # Check if --env is passed via the command line
    env = request.config.getoption("--env", default=None)

    # If --env is not passed, fallback to reading pytest.ini
    if env is None:
        # Read the pytest.ini file
        config_parser = configparser.ConfigParser()
        config_parser.read('pytest.ini')

        # Fetch the environment setting from the [pytest] section
        env = config_parser.get('pytest', 'env', fallback='dev')  # Default to 'dev' if not found
    
    # platform is web by default as it is browser fixtures
    config = load_config(env=env, platform='web')

    # Set up logging based on config
    logging_level = getattr(logging, config.get('logging_level', 'INFO'))
    logging.basicConfig(level=logging_level)

    return config

@pytest.fixture
async def browser():
    """Fixture to create and manage browser instance."""
    async with async_playwright() as playwright:
        web_config = config.get('web', {})
        browser_settings = web_config.get('browser', {})
        
        # Determine browser type
        browser_type_name = browser_settings.get('default', 'chrome').lower()
        if browser_type_name == 'chrome':
            browser_type = playwright.chromium
        elif browser_type_name == 'firefox':
            browser_type = playwright.firefox
        elif browser_type_name == 'webkit':
            browser_type = playwright.webkit
        else:
            browser_type = playwright.chromium  # Default fallback
        
        # Launch browser with appropriate options
        headless = browser_settings.get('headless', True)
        
        browser_instance = await browser_type.launch(headless=headless)

        yield browser_instance
        await browser_instance.close()


@pytest.fixture
async def context(browser, config):
    """Fixture to create and manage browser context."""
    web_config = config.get('web', {})
    
    # Get base URL from environment-specific config
    base_url = web_config.get('base_url', 'http://localhost:3000')
    
    # Create context with configuration
    browser_context = await browser.new_context(
        viewport={"width": 1920, "height": 1080},
        base_url=base_url
    )
    
    # Handle cookies if configured
    cookies_config = web_config.get('cookies', {})
    if cookies_config.get('load_on_start', False):
        cookies_path = cookies_config.get('path', './data/cookies')
        try:
            # Load cookies if file exists
            if os.path.exists(cookies_path):
                with open(cookies_path, 'r') as f:
                    cookies = yaml.safe_load(f)
                    if cookies:
                        await browser_context.add_cookies(cookies)
        except Exception as e:
            logging.warning(f"Failed to load cookies: {e}")
    
    yield browser_context
    
    # Save cookies on exit if configured
    if cookies_config.get('save_on_exit', False):
        cookies_path = cookies_config.get('path', './data/cookies')
        try:
            cookies_dir = os.path.dirname(cookies_path)
            if not os.path.exists(cookies_dir):
                os.makedirs(cookies_dir)
            
            cookies = await browser_context.cookies()
            with open(cookies_path, 'w') as f:
                yaml.dump(cookies, f)
        except Exception as e:
            logging.warning(f"Failed to save cookies: {e}")
    
    await browser_context.close()

@pytest.fixture
async def page(context, config):
    """Fixture to create and manage page."""
    web_config = config.get('web', {})
    
    # Create new page
    page_instance = await context.new_page()
    
    # Configure timeouts from config
    timeouts = web_config.get('timeouts', {})
    default_timeout = web_config.get('default_timeout', 30) * 1000  # Convert to ms
    
    # Set default timeout (prioritize env-specific setting if available)
    page_instance.set_default_timeout(default_timeout)
    
    # Configure other page settings as needed
    
    yield page_instance
    
    # Take screenshot on failure if configured
    screenshots_config = web_config.get('screenshots', {})
    if screenshots_config.get('take_on_failure', False):
        # This will be in the finalizer, but we don't have test result here
        # You would need to implement this with a pytest hook in conftest.py
        pass
    
    await page_instance.close()

@pytest.fixture
async def page_objects(page, config):
    """Fixture to provide page objects for web tests."""
    # Initialize page objects with the page
    base_page = BasePage(page)
    login_page = LoginPage(page)
    
    # Get user credentials from config for potential use in page objects
    web_config = config.get('web', {})
    users = web_config.get('users', {})
    
    # Create a dictionary of page objects and other useful objects
    objects = {
        "base_page": base_page,
        "login_page": login_page,
        "config": config,
        "users": users
        # Add more page objects as needed
    }
    
    return objects