from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class PimPage(BasePage):
    """Covers the PIM (Personnel Information Management) module: adding
    a new employee and searching the employee list. This is the core
    'real workflow' of OrangeHRM, as opposed to just login.
    """

    ADD_EMPLOYEE_BUTTON = (By.XPATH, "//button[contains(text(),'Add')]")
    FIRST_NAME_INPUT = (By.NAME, "firstName")
    LAST_NAME_INPUT = (By.NAME, "lastName")
    SAVE_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    EMPLOYEE_FULL_NAME_HEADER = (By.CSS_SELECTOR, ".employee-name-title")

    EMPLOYEE_NAME_SEARCH_INPUT = (By.CSS_SELECTOR, ".oxd-autocomplete-wrapper input")
    SEARCH_BUTTON = (By.XPATH, "//button[contains(text(),'Search')]")
    RESULT_TABLE_ROWS = (By.CSS_SELECTOR, ".oxd-table-body .oxd-table-row")
    NO_RECORDS_MESSAGE = (By.CSS_SELECTOR, ".oxd-text--span")

    def click_add_employee(self):
        self.click(self.ADD_EMPLOYEE_BUTTON)
        return self

    def add_employee(self, first_name: str, last_name: str):
        self.type_text(self.FIRST_NAME_INPUT, first_name)
        self.type_text(self.LAST_NAME_INPUT, last_name)
        self.click(self.SAVE_BUTTON)
        return self

    def get_employee_full_name(self) -> str:
        return self.get_text(self.EMPLOYEE_FULL_NAME_HEADER)

    def search_employee_by_name(self, name: str):
        self.type_text(self.EMPLOYEE_NAME_SEARCH_INPUT, name)
        self.click(self.SEARCH_BUTTON)
        return self

    def get_result_row_count(self) -> int:
        rows = self.driver.find_elements(*self.RESULT_TABLE_ROWS)
        return len(rows)
