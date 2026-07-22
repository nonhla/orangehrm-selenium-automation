from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    URL = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"

    USERNAME_INPUT = (By.NAME, "username")
    PASSWORD_INPUT = (By.NAME, "password")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    ERROR_ALERT = (By.CSS_SELECTOR, ".oxd-alert-content-text")
    REQUIRED_FIELD_ERROR = (By.CSS_SELECTOR, ".oxd-input-field-error-message")

    def load(self):
        self.driver.get(self.URL)
        return self

    def login(self, username: str, password: str):
        self.type_text(self.USERNAME_INPUT, username)
        self.type_text(self.PASSWORD_INPUT, password)
        self.click(self.SUBMIT_BUTTON)
        return self

    def get_error_message(self) -> str:
        return self.get_text(self.ERROR_ALERT)

    def get_required_field_error(self) -> str:
        return self.get_text(self.REQUIRED_FIELD_ERROR)
