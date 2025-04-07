# conftest.py
import pytest
import os
import sys
import yaml
import glob
import re
from pathlib import Path

# Add project root to sys.path to enable imports
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Define the base directory for locators relative to the project root
LOCATORS_BASE_DIR = Path(__file__).parent / "locators"

# Regex to parse {file > key} syntax - precompile for efficiency
SELECTOR_KEY_REGEX = re.compile(r"\{(.*?)\s*>\s*(.*?)\}")

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

def load_platform_selectors(platform):
    """Loads all YAML selectors for a given platform."""
    platform_locators_dir = LOCATORS_BASE_DIR / platform
    all_selectors = {}
    if not platform_locators_dir.is_dir():
        # Optional: Log a warning if the directory doesn't exist
        # print(f"Warning: Locator directory not found for platform '{platform}': {platform_locators_dir}")
        return all_selectors # Return empty dict if platform dir doesn't exist

    yaml_files = glob.glob(os.path.join(platform_locators_dir, '*.yaml'))

    for file_path in yaml_files:
        file_name_key = os.path.splitext(os.path.basename(file_path))[0]
        try:
            with open(file_path, 'r') as f:
                data = yaml.safe_load(f)
                if data: # Ensure file is not empty
                    all_selectors[file_name_key] = data
        except yaml.YAMLError as e:
            print(f"Error loading YAML file {file_path}: {e}")
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")

    return all_selectors

@pytest.fixture(scope="session")
def selectors(request):
    """
    Session-scoped fixture to load ALL selectors for the target platform
    based on a command-line option '--platform'.
    """
    platform = request.config.getoption("--platform")
    if not platform:
        # Default platform or raise error if not provided
        platform = "web" # Or raise ValueError("Platform must be specified via --platform")
        print(f"Warning: --platform not specified, defaulting to '{platform}'.")

    # Load selectors only once per session for the target platform
    # You might want caching if platform could change mid-session (unlikely with standard pytest runs)
    loaded_selectors = load_platform_selectors(platform)
    if not loaded_selectors:
         print(f"Warning: No selectors loaded for platform '{platform}'. Check directory: {LOCATORS_BASE_DIR / platform}")
    return loaded_selectors

@pytest.fixture(scope="session")
def resolve_selector(selectors):
    """
    Provides a helper function to resolve a '{file > key}' string
    into a locator tuple (type, value) using the loaded selectors.
    """
    def _resolver(selector_key_string):
        match = SELECTOR_KEY_REGEX.match(selector_key_string)
        if not match:
            # Maybe it's not a {file > key} string, could be direct text/value
            # Decide how to handle this case - raise error or return None/original?
            # For now, assume it MUST be in the {file > key} format for element lookups
             raise ValueError(f"Invalid selector format: '{selector_key_string}'. Expected '{{file > key}}'")

        file_key, element_key = match.groups()

        try:
            locator_data = selectors[file_key][element_key]

            if isinstance(locator_data, str):
                # Assume default type is 'css selector' if only string is provided
                return ("css selector", locator_data)
            elif isinstance(locator_data, dict) and 'value' in locator_data:
                # Use specified type or default to 'css selector'
                locator_type = locator_data.get('type', 'css selector').lower()
                return (locator_type, locator_data['value'])
            else:
                raise TypeError(f"Unsupported locator format for '{file_key} > {element_key}' in {file_key}.yaml")

        except KeyError:
            raise KeyError(f"Selector key '{element_key}' not found in '{file_key}.yaml' or file '{file_key}' not loaded/found in platform '{selectors.get('_platform', 'unknown')}'.") # Improve error
        except TypeError:
             raise TypeError(f"File key '{file_key}' (from {file_key}.yaml) does not seem to contain valid selector data or was not loaded correctly.")

    # Add the platform info to the selectors dict for better error messages potentially
    # This is a bit hacky, maybe find a cleaner way if needed
    # selectors['_platform'] = platform_being_used

    return _resolver