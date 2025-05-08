from playwright.sync_api import Page
from pages.registration_page import RegistrationPage
from pages.home_page import HomePage
from pages.checkout_page import CheckoutPage
from pages.profile_page import ProfilePage
from utils.test_data import generate_test_user
import pytest

def test_purchase_flow(page: Page):
    # Initialize page objects
    registration_page = RegistrationPage(page)
    home_page = HomePage(page)
    checkout_page = CheckoutPage(page)
    profile_page = ProfilePage(page)

    # Register new user
    user_data = generate_test_user()
    registration_page.navigate_to_register()
    registration_page.fill_registration_form(user_data)
    registration_page.submit_registration()

    # Set currency to GBP
    home_page.navigate_to_home_page()
    home_page.user_is_logged_in()
    home_page.set_currency_to_gbp()
    total_price=home_page.add_random_item_to_cart_from_subcategories(home_page.get_subcategory_links())
    home_page.go_to_checkout()

    # Checkout process
    checkout_page.confirm_order()
    checkout_page.is_order_successful()
    order_number = checkout_page.extract_order_number()

    # Verify order in order history
    profile_page.navigate_to_order_history()
    profile_page.verify_order_id(order_number)
    order_total = profile_page.get_latest_order_total()

    shipping_cost = 1.59
    assert pytest.approx(order_total + shipping_cost, rel=0.01) == pytest.approx(total_price, rel=0.01)
