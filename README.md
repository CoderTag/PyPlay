# PyPlay
<!-- Playwright and Pytest Framework -->

# Comprehensive Automation Framework

A robust test automation framework that supports UI, API, and visual testing using Playwright, Pytest, and BDD.

## Features

- Page Object Model architecture
- BDD-style tests with pytest-bdd
- Cross-browser testing with Playwright
- BrowserStack integration for additional browser coverage
- Visual testing with Testim
- API testing with schema validation
- Performance monitoring
- Accessibility testing
- Detailed reporting with Allure and pytest-html
- CI/CD integration with GitHub Actions

## Prerequisites

- Python 3.10+
- Node.js 16+
- BrowserStack account (optional)
- Testim account (optional)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/automation-framework.git
cd automation-framework


python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate




automation-framework/
├── conftest.py                  # pytest configuration and fixtures
├── pytest.ini                   # pytest settings
├── requirements.txt             # dependencies
├── .env                         # environment variables (gitignored)
├── README.md                    # documentation
├── features/                    # BDD feature files
│   ├── login.feature
│   ├── checkout.feature
│   └── api_endpoints.feature
├── step_definitions/            # BDD step implementations
│   ├── common_steps.py
│   ├── login_steps.py
│   └── api_steps.py
├── pages/                       # Page Object Models
│   ├── base_page.py
│   ├── login_page.py
│   └── checkout_page.py
├── api/                         # API utilities
│   ├── api_client.py
│   └── endpoints.py
├── utils/                       # Utility functions
│   ├── config_loader.py
│   ├── data_generator.py
│   ├── visual_testing.py
│   └── reporting.py
├── data/                        # Test data
│   ├── test_users.json
│   └── api_payloads/
└── reports/                     # Test results
    ├── html_reports/
    └── allure_reports/



### Description of the Folder Structure

- **conftest.py**: Contains pytest configuration and fixtures shared across tests.
- **pytest.ini**: Contains pytest settings such as test markers and command-line options.
- **requirements.txt**: List of dependencies needed for the project, including testing libraries and frameworks.
- **.env**: Stores environment variables used by the automation framework (gitignored).
- **README.md**: This file, containing the project documentation.
  
### Feature Files (BDD)

Located in the `features/` directory, these `.feature` files define the behavior of the system in a human-readable format using Gherkin syntax. Example feature files:

- `login.feature`: Contains scenarios for logging into the application.
- `checkout.feature`: Contains scenarios for the checkout process in an e-commerce system.
- `api_endpoints.feature`: Defines scenarios for API endpoint tests.

### Step Definitions (BDD)

The `step_definitions/` directory holds the Python files that implement the step definitions for the feature files. Example step definitions:

- `common_steps.py`: Common step implementations used across multiple feature files.
- `login_steps.py`: Step implementations specific to the login feature.
- `api_steps.py`: Step implementations for API tests.

### Page Object Models (POM)

The `pages/` directory contains the Page Object Models (POM), which represent the UI pages and encapsulate the interactions with the web elements on those pages.

- `base_page.py`: Contains common methods for interacting with web pages.
- `login_page.py`: Represents the login page of the application.
- `checkout_page.py`: Represents the checkout page of the application.

### API Utilities

The `api/` directory provides utilities for interacting with the API endpoints.

- `api_client.py`: Contains methods for sending HTTP requests and handling responses.
- `endpoints.py`: Defines the API endpoints used in the tests.

### Utility Functions

Located in the `utils/` directory, these are helper functions that are used throughout the framework.

- `config_loader.py`: Loads configuration files.
- `data_generator.py`: Generates test data dynamically.
- `visual_testing.py`: Provides functionality for visual regression testing.
- `reporting.py`: Generates test reports.

### Test Data

The `data/` directory contains the test data required for running the tests.

- `test_users.json`: JSON file containing user credentials or other related test data.
- `api_payloads/`: Directory containing predefined API request payloads.

### Test Reports

Test results are stored in the `reports/` directory:

- `html_reports/`: Contains HTML format test reports.
- `allure_reports/`: Contains Allure format reports for detailed test results.

## Prerequisites

Before running the tests, make sure to install the required dependencies. You can do this by running:

```bash
pip install -r requirements.txt
