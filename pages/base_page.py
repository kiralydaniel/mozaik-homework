from playwright.sync_api import Page

class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.base_url = "https://automationteststore.com"

    def navigate(self, path: str) -> None:
        self.page.goto(f"{self.base_url}{path}") 
