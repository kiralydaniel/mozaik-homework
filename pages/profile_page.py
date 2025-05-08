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
        # Get all order rows
        order_containers = self.page.locator("div.container-fluid.mt20")
        
        # Get the first (most recent) order row
        latest_order = order_containers.first
        
        # Within this row, find the total
        total_cell = latest_order.locator("td", has_text="Total:")
        total_text = total_cell.inner_text()
        
        # Extract the price from the text
        price = total_text.replace("Total:", "").replace("£", "").replace(",", "").strip()
        return float(price)
