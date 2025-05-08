from playwright.sync_api import Page
from pages.registration_page import RegistrationPage
from pages.home_page import HomePage
from utils.test_data import generate_test_user

def test_purchase_flow(page: Page):
    # Initialize page objects
    registration_page = RegistrationPage(page)
    home_page = HomePage(page)

    # Register new user
    user_data = generate_test_user()
    registration_page.navigate_to_register()
    registration_page.fill_registration_form(user_data)
    registration_page.submit_registration()

    # Set currency to GBP
    home_page.navigate_to_home_page()
    home_page.set_currency_to_gbp()
