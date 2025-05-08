from .base_page import BasePage
from playwright.sync_api import expect

class CheckoutPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.confirm_order_button = page.get_by_role("button", name="Confirm Order")
        self.order_success_message = page.get_by_text("Your Order Has Been Processed!")

    def confirm_order(self):
        self.confirm_order_button.click()

    def is_order_successful(self):
        expect(self.order_success_message).to_be_visible()
    
    def extract_order_number(self):
        confirmation_text = self.page.get_by_text("Your order #").text_content().strip()
        order_number = confirmation_text.split("#")[1].split()[0]
        return order_number
