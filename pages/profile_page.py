from .base_page import BasePage
from playwright.sync_api import expect

class ProfilePage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    def navigate_to_order_history(self):
        self.navigate("/index.php?rt=account/history")

    def verify_order_id(self, order_number):
        expect(self.page.get_by_text(f"Order ID: #{order_number}")).to_be_visible()

    def get_latest_order_total(self) -> float:
        total_text = self.page.locator("td", has_text="Total:").inner_text()
        price = total_text.replace("Total:", "").replace("£", "").replace(",", "").strip()
        return float(price)
