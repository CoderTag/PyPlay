#By using the pytest_plugins variable in the steps/__init__.py file, 
# pytest will automatically discover and register the step definitions in common_steps.py. 
# This approach ensures that the step definitions are globally accessible 
# without needing to import them in conftest.py.

pytest_plugins = [
    "tests.steps.common_steps",
    "tests.steps.api_steps",
    "tests.steps.navigation_steps",
    "tests.steps.ui_steps",
]