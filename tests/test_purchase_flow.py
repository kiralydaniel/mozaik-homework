from playwright.sync_api import Page
from pages.registration_page import RegistrationPage
from pages.home_page import HomePage
from pages.checkout_page import CheckoutPage
from pages.profile_page import ProfilePage
from pages.login_page import LoginPage
from utils.test_data import generate_test_user, get_existing_user
import pytest

@pytest.mark.parametrize("use_existing_user", [True, False], ids=["existing_user", "new_user"])
def test_purchase_flow(page: Page, use_existing_user: bool):
    # Initialize page objects
    registration_page = RegistrationPage(page)
    login_page = LoginPage(page)
    home_page = HomePage(page)
    checkout_page = CheckoutPage(page)
    profile_page = ProfilePage(page)

    if use_existing_user:
        # Use existing user
        user_data = get_existing_user()
        if not user_data['login_name'] or not user_data['password']:
            pytest.skip("Test user credentials not set in environment variables")
        login_page.navigate_to_login()
        login_page.login(user_data['login_name'], user_data['password'])
    else:
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
    
    # Get shipping fee
    shipping_cost = checkout_page.get_shipping_fee()

    # Checkout process
    checkout_page.confirm_order()
    checkout_page.is_order_successful()
    order_number = checkout_page.extract_order_number()

    # Verify order in order history
    profile_page.navigate_to_order_history()
    profile_page.verify_order_id(order_number)
    order_total = profile_page.get_latest_order_total()

    # Verify total price
    assert pytest.approx(order_total + shipping_cost, rel=0.01) == pytest.approx(total_price, rel=0.01)
