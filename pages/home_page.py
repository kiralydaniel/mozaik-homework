from .base_page import BasePage
from playwright.sync_api import expect

class HomePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        
        # Locators
        self.currency_dropdown = page.locator("a").filter(has_text="$ US Dollar").first
        self.currency_gbp = page.get_by_role("link", name="£ Pound Sterling")
        self.profile_menu = page.get_by_role("link", name="Welcome back")
        self.subcategory_links_locator = self.page.locator("div.subcategories a")

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
