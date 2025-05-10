from .base_page import BasePage
from playwright.sync_api import expect
from utils.test_data import clean_price_text

class CheckoutPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.confirm_order_button = page.get_by_role("button", name="Confirm Order")
        self.order_success_message = page.get_by_text("Your Order Has Been Processed!")
        self.shipping_text = page.locator("text=Flat Shipping Rate:").locator("xpath=../following-sibling::td/span[contains(@class, 'bold')]")


    def confirm_order(self) -> None:
        self.confirm_order_button.click()

    def is_order_successful(self) -> None:
        expect(self.order_success_message).to_be_visible()
    
    def extract_order_number(self) -> str:
        confirmation_text = self.page.get_by_text("Your order #").text_content().strip()
        order_number = confirmation_text.split("#")[1].split()[0]
        return order_number
    
    def get_shipping_fee(self) -> float:
        expect(self.shipping_text).to_be_visible()
        shipping_fee_text = self.shipping_text.inner_text()

        return clean_price_text(shipping_fee_text)
