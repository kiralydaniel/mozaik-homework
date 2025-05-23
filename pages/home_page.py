from .base_page import BasePage
from playwright.sync_api import expect, Locator
from typing import List, Dict, Optional
from utils.test_data import clean_price_text, extract_product_id_from_url
import random

class HomePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        
        # Locators
        self.currency_dropdown = page.locator("a").filter(has_text="$ US Dollar").first
        self.currency_gbp = page.get_by_role("link", name="£ Pound Sterling")
        self.currency_euro = page.get_by_role("link", name="€ Euro")
        self.currency_usd = page.get_by_role("link", name="$ US Dollar")
        self.profile_menu = page.get_by_role("link", name="Welcome back")
        self.subcategory_links_locator = self.page.locator("div.subcategories a")
        self.product_items = page.locator(".thumbnails.grid .thumbnail")
        self.add_to_cart_button = page.locator("#product a.cart")
        self.size_option = page.get_by_text("3 UK")
        self.description = page.get_by_role("link", name="Description")
        self.product_price = self.page.locator("span.total-price")
        self.cart_checkout_button = page.locator("#cart_checkout1")
        self.minimum_quantity = page.get_by_text("(This product has a minimum")
        self.fragrance_type = page.get_by_text("Fragrance Type", exact=True)
        self.fragrance_options = page.locator("input[type='checkbox'][name^='option[335]']")
        self.scent_options = page.get_by_text("Choose Scent")
        self.added_product_ids = set()

    def user_is_logged_in(self) -> None:
        expect(self.profile_menu).to_be_visible()

    def navigate_to_home_page(self) -> None:
        self.navigate("/")

    def set_currency(self, currency: str = "GBP") -> None:
        currency_map = {
        "GBP": self.currency_gbp,
        "EUR": self.currency_euro,
        "USD": self.currency_usd
        }

        if currency not in currency_map:
            raise ValueError(f"Unsupported currency: {currency}. Supported currencies are: {', '.join(currency_map.keys())}")
        
        expect(self.currency_dropdown).to_be_visible()
        self.currency_dropdown.hover()
        expect(currency_map[currency]).to_be_visible()
        currency_map[currency].click()

    def get_subcategory_links(self) -> List[Dict[str, str]]:

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
        price_text = self.product_price.inner_text()

        return clean_price_text(price_text)

    
    def select_fragrance_option(self, option_id: Optional[str] = None) -> bool:
        """
        Select a fragrance option by ID or randomly if none provided
        Options from HTML: option335722 (Eau de Cologne), option335721 (Eau de Toilette), option335720 (Eau de Parfum)
        """
        # Wait for fragrance options to be visible
        self.fragrance_options.first.wait_for(state="visible")
        
        # Get all available fragrance options
        options = self.fragrance_options.all()
        
        if not options:
            print("No fragrance options found")
            return False
            
        if option_id:
            # Find the option with the specified ID
            for option in options:
                if option.get_attribute("id") == option_id:
                    option.check()
                    print(f"Selected fragrance option: {option_id}")
                    return True
            print(f"Option with ID {option_id} not found")
            return False
        else:
            # Select a random option
            random_option = random.choice(options)
            option_id = random_option.get_attribute("id")
            random_option.check()
            print(f"Selected random fragrance option: {option_id}")
            return True

    def get_in_stock_products(self) -> List[Locator]:

        products = self.product_items.all()
        return [p for p in products if not p.locator("span.nostock").is_visible()]

    def handle_product_options(self, subcategory_name: str) -> bool:

        # Handle required size option for shoes
        if subcategory_name == "Shoes":
            if self.size_option.is_visible():
                self.size_option.click()

        # Handle fragrance options
        if subcategory_name == "Women":
            if self.fragrance_type.is_visible():
                if not self.select_fragrance_option():
                    return False
            elif self.scent_options.is_visible():
                return False

        # Handle products with more than one minimum quantity
        if self.minimum_quantity.is_visible():
            print("Product has a minimum quantity, skipping.")
            return False

        # Check for "Add to Cart" button (to skip 'Call to order' cases)
        if not self.add_to_cart_button.is_visible():
            print("No Add to Cart button, skipping.")
            return False
            
        return True

    def try_to_add_product_to_cart(self, product: Locator, subcategory_name: str) -> float:
        product_href = product.locator("a").first.get_attribute("href")
        product_id = extract_product_id_from_url(product_href)
        if product_id in self.added_product_ids:
            print(f"Product '{product_href}' already added, skipping.")
            return 0.0

        product.click()
        self.description.wait_for(state="visible")
        
        if not self.handle_product_options(subcategory_name):
            self.page.go_back()
            return 0.0
        
        # Get product price
        product_price = self.get_product_price()
        
        # Click Add to Cart
        self.add_to_cart_button.click()
        print(f"Added product from subcategory: {subcategory_name}, path: {product_href}")
        
        self.added_product_ids.add(product_id)
        return product_price

    def add_product_from_subcategory(self, subcategory: Dict[str, str]) -> float:
        self.navigate(subcategory["path"])
        in_stock_products = self.get_in_stock_products()
        
        if not in_stock_products:
            print(f"No in-stock products in subcategory: {subcategory['name']}")
            return 0.0

        # Try products until one is successfully added or we run out of products
        remaining_products = in_stock_products.copy()
        while remaining_products:
            random_product = random.choice(remaining_products)
            remaining_products.remove(random_product)

            product_price = self.try_to_add_product_to_cart(random_product, subcategory["name"])

            if product_price > 0:
                return product_price
                
        print(f"No suitable product to add from subcategory: {subcategory['name']}")
        return 0.0

    def add_random_item_to_cart_from_subcategories(self, subcategories: List[Dict[str, str]]) -> tuple[float, int]:
        total_price = 0.0
        product_count = 0

        for subcategory in subcategories:
            product_price = self.add_product_from_subcategory(subcategory)
            if product_price > 0:
                total_price += product_price
                product_count += 1

        return round(total_price, 2), product_count
    
    def go_to_checkout(self) -> None:
        self.cart_checkout_button.click()