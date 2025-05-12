from .base_page import BasePage

class RegistrationPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        
        # Locators
        self.first_name_input = page.locator('#AccountFrm_firstname')
        self.last_name_input = page.locator("#AccountFrm_lastname")
        self.email_input = page.locator("#AccountFrm_email")
        self.telephone_input = page.locator("#AccountFrm_telephone")
        self.address_input = page.locator("#AccountFrm_address_1")
        self.city_input = page.locator("#AccountFrm_city")
        self.region_select = page.locator("#AccountFrm_zone_id")
        self.postcode_input = page.locator("#AccountFrm_postcode")
        self.login_name_input = page.locator("#AccountFrm_loginname")
        self.password_input = page.locator("#AccountFrm_password")
        self.password_confirm_input = page.locator("#AccountFrm_confirm")
        self.agree_checkbox = page.get_by_role("checkbox", name="I have read and agree to the")
        self.continue_button = page.get_by_role("button", name="Continue")

    def fill_registration_form(self, user_data: dict) -> None:
        self.first_name_input.fill(user_data["first_name"])
        self.last_name_input.fill(user_data["last_name"])
        self.email_input.fill(user_data["email"])
        self.telephone_input.fill(user_data["telephone"])
        self.address_input.fill(user_data["address"])
        self.city_input.fill(user_data["city"])
        self.region_select.select_option(value=user_data["region"])
        self.postcode_input.fill(user_data["postcode"])
        self.login_name_input.fill(user_data["login_name"])
        self.password_input.fill(user_data["password"])
        self.password_confirm_input.fill(user_data["password"])
        self.agree_checkbox.check()
    
    def navigate_to_register(self) -> None:
        self.navigate("/index.php?rt=account/create")

    def submit_registration(self) -> None:
        self.continue_button.click()
