# E-commerce Web Application

This project is an automated test suite for an e-commerce web application using Playwright with Python.

## Features

- User registration and login
- Product browsing and shopping cart management
- Checkout process
- Order history verification
- Currency selection (GBP, EUR, USD support)
- Automated test scenarios for both new and existing users

## Prerequisites

- Python 3.x
- Playwright
- pytest

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install Playwright browsers:
```bash
playwright install
```

## Environment Variables

For running tests with existing users, set the following environment variables:
- `LOGIN_NAME`: Login name for the test user
- `PASSWORD`: Password for the test user

## Running Tests

To run all tests:
```bash
pytest
```

To run tests with visible browser:
```bash
pytest --headed
```

To run specific test (new user):
```bash
pytest "tests/test_purchase_flow.py::test_purchase_flow[chromium-new_user]"
```

To run specific test (existing user):
```bash
pytest "tests/test_purchase_flow.py::test_purchase_flow[chromium-existing_user]"
```

To generate HTML test report:
```bash
pytest --html=report.html --self-contained-html
```

## Test Structure

The test suite is organized into page objects:
- `RegistrationPage`: Handles user registration
- `LoginPage`: Manages user login
- `HomePage`: Handles product browsing and cart management
- `CheckoutPage`: Manages the checkout process
- `ProfilePage`: Handles order history and verification

## Test Scenarios

The main test scenario (`test_purchase_flow`) covers:
1. User authentication (new registration or existing user login)
2. Currency selection (GBP as default, but works with EUR and USD)
3. Adding items to cart
4. Checkout process
5. Order verification
6. Item quantity and Price validation including shipping costs

## Project Structure

```
├── pages/
│   ├── registration_page.py
│   ├── login_page.py
│   ├── home_page.py
│   ├── checkout_page.py
│   └── profile_page.py
├── tests/
│   └── test_purchase_flow.py
├── utils/
│   └── test_data.py
└── README.md
```
