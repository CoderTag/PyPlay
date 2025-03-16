# conftest.py
import os
import json
import pytest
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

# Load environment variables
load_dotenv()

def pytest_addoption(parser):
    parser.addoption("--browser", default="chromium", help="Browser to run tests")
    parser.addoption("--env", default="staging", help="Environment to run tests")
    parser.addoption("--headless", action="store_true", default=False, help="Run in headless mode")
    parser.addoption("--browserstack", action="store_true", default=False, help="Run on BrowserStack")
    parser.addoption("--visual", action="store_true", default=False, help="Run visual tests")

@pytest.fixture(scope="session")
def config(request):
    """Return test configuration"""
    browser_name = request.config.getoption("--browser")
    env_name = request.config.getoption("--env")
    headless = request.config.getoption("--headless")
    use_browserstack = request.config.getoption("--browserstack")
    run_visual = request.config.getoption("--visual")
    
    # Load environment configuration
    with open(f'config/{env_name}.json') as config_file:
        env_config = json.load(config_file)
    
    config = {
        "browser": browser_name,
        "headless": headless,
        "use_browserstack": use_browserstack,
        "run_visual": run_visual,
        "base_url": env_config["base_url"],
        "api_base_url": env_config["api_base_url"],
        "users": env_config["users"]
    }
    
    return config

@pytest.fixture(scope="session")
def browser_context(config):
    """Create browser context based on configuration"""
    with sync_playwright() as playwright:
        if config["use_browserstack"]:
            # BrowserStack setup
            browser = _setup_browserstack(playwright, config)
        else:
            # Local browser setup
            browser_type = getattr(playwright, config["browser"])
            browser = browser_type.launch(headless=config["headless"])
        
        # Create a new context for each test session
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            record_video_dir="./videos/" if not config["use_browserstack"] else None
        )
        
        # Setup context defaults
        context.set_default_timeout(15000)  # 15 seconds
        
        yield context
        
        # Cleanup
        context.close()
        browser.close()

def _setup_browserstack(playwright, config):
    """Setup BrowserStack configuration"""
    # BrowserStack configuration
    from browserstack.local import Local
    
    bs_local = None
    if os.environ.get("BS_LOCAL", "false").lower() == "true":
        bs_local = Local()
        bs_local_args = {"key": os.environ["BROWSERSTACK_ACCESS_KEY"]}
        bs_local.start(**bs_local_args)
    
    capabilities = {
        'browser': config["browser"],
        'os': 'Windows',
        'os_version': '10',
        'name': 'Automation Test',
        'build': 'Build-1',
        'browserstack.username': os.environ["BROWSERSTACK_USERNAME"],
        'browserstack.accessKey': os.environ["BROWSERSTACK_ACCESS_KEY"],
        'browserstack.local': 'true' if bs_local else 'false',
    }
    
    # Connect to BrowserStack
    cdp_url = f"wss://cdp.browserstack.com/playwright?caps={json.dumps(capabilities)}"
    browser = playwright.chromium.connect_over_cdp(cdp_url)
    
    return browser

@pytest.fixture
def page(browser_context):
    """Create a new page for each test"""
    page = browser_context.new_page()
    
    # Set up page-level event listeners for debugging
    page.on("console", lambda msg: print(f"BROWSER CONSOLE: {msg.text}"))
    page.on("pageerror", lambda err: print(f"BROWSER ERROR: {err}"))
    
    yield page
    
    # Cleanup
    page.close()

@pytest.fixture
def api_context(config):
    """Create API testing context"""
    from api.api_client import ApiClient
    
    api_client = ApiClient(
        base_url=config["api_base_url"],
        headers={"Content-Type": "application/json"}
    )
    
    yield api_client