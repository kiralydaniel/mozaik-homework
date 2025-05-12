from .base_page import BasePage
from playwright.sync_api import expect

class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.login_button = page.get_by_role("button", name="Login")
        self.login_input = page.locator("#loginFrm_loginname")
        self.password_input = page.locator("#loginFrm_password")

    def navigate_to_login(self) -> None:
        self.navigate("/index.php?rt=account/login")
        expect(self.password_input).to_be_visible()

    def login(self, username: str, password: str) -> None:
        self.login_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()