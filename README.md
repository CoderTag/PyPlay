# PyPlay : Playwright and Pytest Framework

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
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install browsers for Playwright:
```bash
playwright install
```

5. Create a .env file with your credentials:
```bash
BROWSERSTACK_USERNAME=your_username
BROWSERSTACK_ACCESS_KEY=your_access_key
TESTIM_API_URL=https://api.testim.io
TESTIM_PROJECT_ID=your_project_id
TESTIM_API_TOKEN=your_api_token
```

6. Running Tests
Basic Usage
```bash
python run_tests.py
```

7. Advanced Usage
```bash
python run_tests.py --browser firefox --env staging --headless --tags "smoke" --report allure --parallel 2

Options

--browser: Choose between chromium, firefox, or webkit
--env: Choose the environment (dev, staging, prod)
--headless: Run in headless mode
--browserstack: Run on BrowserStack
--visual: Run visual tests
--parallel: Number of parallel workers
--tags: Filter tests by tags
--report: Report type (html or allure)
```

8. Project Structure
```bash
automation-framework/
├── conftest.py                  # pytest configuration and fixtures
├── pytest.ini                   # pytest settings
├── requirements.txt             # dependencies
├── .env                         # environment variables (gitignored)
├── README.md                    # documentation
├── features/                    # BDD feature files
├── step_definitions/            # BDD step implementations
├── pages/                       # Page Object Models
├── api/                         # API utilities
├── utils/                       # Utility functions
├── data/                        # Test data
└── reports/                     # Test results

Detailed View

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

```

9. Best Practices

- Keep page objects focused on UI interactions
- Use explicit waits for reliable element interactions
- Implement proper error handling
- Use data-driven tests for comprehensive coverage
- Write clear and descriptive BDD scenarios
- Use tags to organize tests
- Review and analyze test results regularly

9. Contributing

- Fork the repository
- Create your feature branch (git checkout -b feature/amazing-feature)
- Commit your changes (git commit -m 'Add some amazing feature')
- Push to the branch (git push origin feature/amazing-feature)
- Open a Pull Request

10. Resources for further study
## Resources for Further Study

### Popular Resources

1. **Playwright Documentation**
   - https://playwright.dev/docs/intro
   - Official documentation covering all aspects of Playwright

2. **Pytest Documentation**
   - https://docs.pytest.org/
   - Comprehensive guide to pytest testing framework

3. **Pytest-BDD Documentation**
   - https://pytest-bdd.readthedocs.io/
   - Guide to behavior-driven development with pytest

4. **BrowserStack Documentation**
   - https://www.browserstack.com/docs/
   - Official documentation for BrowserStack integration

5. **Testim Documentation**
   - https://www.testim.io/docs/
   - Visual testing capabilities and integration

### Underrated Resources

1. **Playwright Best Practices**
   - https://playwright.dev/docs/best-practices
   - Lesser-known tips and tricks for Playwright

2. **The Screenplay Pattern**
   - https://serenity-js.org/handbook/design/screenplay-pattern
   - Advanced design pattern for test automation

3. **Test Data Management Strategies**
   - https://www.ministryoftesting.com/dojo/lessons/test-data-management
   - In-depth discussion on test data management

4. **Visual Testing Comparison**
   - https://applitools.com/blog/visual-testing-comparison/
   - Detailed comparison of visual testing approaches

5. **Accessibility Testing Automation**
   - https://marcysutton.com/accessibility-testing-with-axe-core
   - Guide to implementing accessibility testing

### GitHub Repositories

1. **Playwright Python Examples**
   - https://github.com/microsoft/playwright-python/tree/main/examples
   - Official examples by Microsoft

2. **Pytest-BDD Examples**
   - https://github.com/pytest-dev/pytest-bdd/tree/master/examples
   - Examples demonstrating pytest-bdd usage

3. **Comprehensive Test Framework**
   - https://github.com/AutomationPanda/playwright-pytest-demo
   - Well-structured Playwright with pytest example

4. **Playwright Test Patterns**
   - https://github.com/microsoft/playwright-test-pattern
   - Best practices for test organization

5. **Allure Report Examples**
   - https://github.com/allure-examples/allure-pytest-example
   - Examples of Allure reporting with pytest

### AI Tools for Improving Automation

1. **Applitools Eyes**
   - https://applitools.com/
   - AI-powered visual testing that can detect visual regressions

2. **Testim Automate**
   - https://www.testim.io/
   - AI-powered test automation that can generate and maintain tests

3. **Mabl**
   - https://www.mabl.com/
   - Intelligent test automation with self-healing capabilities

4. **Functionize**
   - https://www.functionize.com/
   - AI-powered testing platform that can understand application changes

5. **Playwright Inspector**
   - Built into Playwright
   - AI-assisted test recording and debugging

6. **Deque Axe**
   - https://www.deque.com/axe/
   - AI-powered accessibility testing tool

By integrating these tools and approaches, you can build a comprehensive automation framework that supports UI, API, and visual testing while providing robust reporting and analysis capabilities.

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
