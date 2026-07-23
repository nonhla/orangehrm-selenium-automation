from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class DashboardPage(BasePage):
    """Represents the page landed on right after a successful login.
    Used mainly to confirm login succeeded and as a jumping-off point
    to other modules (PIM, Admin, Leave, etc.) via the side menu.
    """

    HEADER_TITLE = (By.CSS_SELECTOR, "h6.oxd-topbar-header-breadcrumb-module")
    USER_DROPDOWN = (By.CSS_SELECTOR, ".oxd-userdropdown-tab")
    LOGOUT_LINK = (By.LINK_TEXT, "Logout")
    # normalize-space(.) rather than text()='PIM': text() only matches direct
    # text nodes, so if the label is ever wrapped in a nested element this
    # still matches, whereas an exact text() equality check would silently
    # fail to find anything.
    PIM_MENU_ITEM = (By.XPATH, "//span[normalize-space(.)='PIM']")

    def get_header_title(self) -> str:
        return self.get_text(self.HEADER_TITLE)

    def logout(self):
        self.click(self.USER_DROPDOWN)
        self.click(self.LOGOUT_LINK)
        return self

    def go_to_pim(self):
        self.click(self.PIM_MENU_ITEM)
        # Confirm navigation via URL rather than guessing at page-specific
        # text — the screenshot evidence showed the Employee List page was
        # actually loading fine; it was the guessed header text that was
        # wrong, not the navigation itself. The URL is a much more stable
        # thing to assert on than copy that can vary by OrangeHRM version.
        WebDriverWait(self.driver, 15).until(
            EC.url_contains("viewEmployeeList")
        )
        return self
