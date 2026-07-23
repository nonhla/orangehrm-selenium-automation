from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class PimPage(BasePage):
    """Covers the PIM (Personnel Information Management) module: adding
    a new employee and searching the employee list. This is the core
    'real workflow' of OrangeHRM, as opposed to just login.
    """

    # Scoped to the exact button structure confirmed from the live page:
    # a secondary-style oxd-button containing a bi-plus icon. This is far
    # less likely to accidentally match an unrelated element than a bare
    # text-contains check, and doesn't depend on "Add" being a direct vs.
    # nested text node (which is what broke the earlier text()-based guess).
    ADD_EMPLOYEE_BUTTON = (
        By.XPATH,
        "//button[contains(@class,'oxd-button--secondary')][.//i[contains(@class,'bi-plus')]]"
    )
    FIRST_NAME_INPUT = (By.NAME, "firstName")
    LAST_NAME_INPUT = (By.NAME, "lastName")
    SAVE_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    # Confirmed from the live personal-details page: the name renders as
    # an <h6> inside a div.orangehrm-edit-employee-name container. Scoping
    # to that stable container class rather than the OXD text-utility
    # classes on the h6 itself (which are more likely to shift between
    # versions than a semantic container class).
    EMPLOYEE_FULL_NAME_HEADER = (By.CSS_SELECTOR, ".orangehrm-edit-employee-name h6")

    EMPLOYEE_NAME_SEARCH_INPUT = (By.CSS_SELECTOR, ".oxd-autocomplete-wrapper input")
    # The employee-name field is an autocomplete: typing text alone does
    # NOT filter results on its own — the field must have a suggestion
    # selected from the dropdown it populates, or the search treats it as
    # empty. This locator targets that dropdown's option list.
    AUTOCOMPLETE_OPTION = (By.CSS_SELECTOR, ".oxd-autocomplete-dropdown .oxd-autocomplete-option")
    SEARCH_BUTTON = (By.XPATH, "//button[contains(., 'Search')]")
    RESULT_TABLE_ROWS = (By.CSS_SELECTOR, ".oxd-table-body .oxd-table-row")
    NO_RECORDS_MESSAGE = (By.CSS_SELECTOR, ".oxd-text--span")

    def click_add_employee(self):
        # Longer timeout than the base default: CI's headless Chrome has
        # occasionally needed more than 10s for this page's client-side
        # render to finish before the button becomes interactable.
        self.click(self.ADD_EMPLOYEE_BUTTON, timeout=20)
        return self

    def add_employee(self, first_name: str, last_name: str):
        self.type_text(self.FIRST_NAME_INPUT, first_name)
        self.type_text(self.LAST_NAME_INPUT, last_name)
        self.click(self.SAVE_BUTTON)
        # Confirm the save actually navigated to the personal-details page
        # via URL rather than immediately trying to read the name header —
        # same class of race condition as the earlier PIM navigation fix.
        WebDriverWait(self.driver, 15).until(
            EC.url_contains("viewPersonalDetails")
        )
        return self

    def get_employee_full_name(self) -> str:
        # get_nonblank_text rather than get_text: the name populates via a
        # follow-up API call after the page itself has already rendered,
        # so a plain visibility check can catch it mid-render, still blank.
        return self.get_nonblank_text(self.EMPLOYEE_FULL_NAME_HEADER, timeout=15)

    def search_employee_by_name(self, name: str):
        self.type_text(self.EMPLOYEE_NAME_SEARCH_INPUT, name)
        try:
            # Confirmed via live inspection that this locator is correct
            # (.oxd-autocomplete-dropdown .oxd-autocomplete-option matches
            # the real suggestion rows). The earlier 5s timeout was too
            # short: this dropdown depends on a live network round-trip
            # to OrangeHRM's server as you type, which can take longer
            # than that — especially from a CI runner. If a real match
            # exists, select it from the dropdown so the field is
            # actually bound to that employee before searching.
            self.click(self.AUTOCOMPLETE_OPTION, timeout=15)
        except Exception:
            # No dropdown suggestion appeared — expected for the
            # "no such employee" case, where we want zero results anyway.
            pass
        self.click(self.SEARCH_BUTTON)
        return self

    def get_result_row_count(self) -> int:
        rows = self.driver.find_elements(*self.RESULT_TABLE_ROWS)
        return len(rows)
