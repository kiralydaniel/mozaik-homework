from .base_page import BasePage
from playwright.sync_api import expect
import random

class HomePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        
        # Locators
        self.currency_dropdown = page.locator("a").filter(has_text="$ US Dollar").first
        self.currency_gbp = page.get_by_role("link", name="£ Pound Sterling")
        self.profile_menu = page.get_by_role("link", name="Welcome back")
        self.subcategory_links_locator = self.page.locator("div.subcategories a")
        self.product_items = page.locator(".thumbnails.grid .thumbnail")
        self.add_to_cart_button = page.locator("#product a.cart")
        self.size_option = page.get_by_text("3 UK")
        self.description = page.get_by_role("link", name="Description")
        self.product_price = self.page.locator("span.total-price")

    def user_is_logged_in(self):
        expect(self.profile_menu).to_be_visible()

    def navigate_to_home_page(self):
        self.navigate("/")

    def set_currency_to_gbp(self):
        expect(self.currency_dropdown).to_be_visible()
        self.currency_dropdown.hover()
        expect(self.currency_gbp).to_be_visible()
        self.currency_gbp.click()

    def get_subcategory_links(self) -> list[dict]:
        subcategory_links = self.subcategory_links_locator
        count = subcategory_links.count()

        subcategories = []
        for i in range(count):
            element = subcategory_links.nth(i)
            name = element.inner_text().strip()
            href = element.get_attribute("href")
            if href and href.startswith(self.base_url):
                path = href.replace(self.base_url, "")
                subcategories.append({"name": name, "path": path})
        
        return subcategories
    
    def get_product_price(self) -> float:
        self.product_price.wait_for(state="visible")
        price_text = self.product_price.inner_text().replace("£", "").replace(",", "").strip()
        
        return float(price_text)

    def add_random_item_to_cart_from_subcategories(self, subcategories: list[dict]) -> float:
        total_price = 0.0
        for subcategory in subcategories:
            self.navigate(subcategory["path"])

            products = self.product_items.all()
            in_stock_products = [p for p in products if not p.locator("span.nostock").is_visible()]
            
            if not in_stock_products:
                print(f"No in-stock products in subcategory: {subcategory['name']}")
                continue

            max_attempts = len(in_stock_products)
            for attempt in range(max_attempts):
                random_product = random.choice(in_stock_products)
                random_product.click()

                self.description.wait_for(state="visible")

                # Handle required size option for shoes
                if subcategory["name"] == "Shoes":
                    if self.size_option.is_visible():
                        self.size_option.click()

                # Check for "Add to Cart" button (to skip 'Call to order' cases)
                if not self.add_to_cart_button.is_visible():
                    print("No Add to Cart button, skipping.")
                    in_stock_products.remove(random_product)
                    self.page.go_back()
                    continue

                # Add product price to total
                total_price += self.get_product_price()

                # Click Add to Cart
                self.add_to_cart_button.click()
                print(f"Added product from subcategory: {subcategory['name']}")
                break
            else:
                print(f"No suitable product to add from subcategory: {subcategory['name']}")

        return total_price
