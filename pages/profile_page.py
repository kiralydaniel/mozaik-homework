from .base_page import BasePage
from playwright.sync_api import expect
from utils.test_data import clean_price_text

class ProfilePage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    def navigate_to_order_history(self) -> None:
        self.navigate("/index.php?rt=account/history")

    def verify_order_id(self, order_number) -> None:
        expect(self.page.get_by_text(f"Order ID: #{order_number}")).to_be_visible()

    def get_latest_order_total(self) -> tuple[float, int]:
        # Get all order rows
        order_containers = self.page.locator("div.container-fluid.mt20")
        
        # Get the first (most recent) order row
        latest_order_price = order_containers.first
        
        # Within this row, find the total price
        total_price_cell = latest_order_price.locator("td", has_text="Total:")
        total_price_text = total_price_cell.inner_text()
        raw_price_text = total_price_text.replace("Total:", "")

        total_product_quantity_cell = latest_order_price.locator("td", has_text="Products:")
        total_quantity_text = total_product_quantity_cell.inner_text()
        raw_quantity_text = total_quantity_text.replace("Products:", "")

        return clean_price_text(raw_price_text), int(raw_quantity_text)
