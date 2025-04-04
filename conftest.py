# conftest.py

import pytest
import os
import sys

# Add project root to sys.path to enable imports
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Import fixtures from central location
from fixtures.browser_fixtures import browser, context, page, page_objects, config

# Platform selection through command line options
def pytest_addoption(parser):
    parser.addoption("--platform", default="web", 
                     choices=["web", "mobile", "api"],
                     help="Specify the platform to run tests against")
    parser.addoption("--env", default="dev", 
                    choices=["dev", "qa", "prod"],
                    help="Specify the environment to run tests against")

# Conditionally load platform-specific fixtures and hooks
@pytest.fixture(scope="session")
def platform(request):
    return request.config.getoption("--platform")

@pytest.fixture(scope="session")
def environment(request):
    return request.config.getoption("--env")

# We only need to configure the BDD paths once at the session level
def pytest_configure(config):
    config.option.keyword = f"{config.getoption('platform')}/"

# Hook to skip tests not meant for the selected platform
def pytest_collection_modifyitems(config, items):
    platform = config.getoption("--platform")
    
    for item in items:
        # Skip tests not meant for the selected platform
        if f"/{platform}/" not in item.nodeid and f"{platform}_" not in item.nodeid:
            skip_marker = pytest.mark.skip(reason=f"Test not for {platform} platform")
            item.add_marker(skip_marker)