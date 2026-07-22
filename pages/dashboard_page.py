from selenium.webdriver.common.by import By
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
    # Landmark used to confirm navigation actually completed before handing
    # control back — without this, a broken PIM_MENU_ITEM locator wouldn't
    # fail here; it would fail confusingly later, on whatever PIM element
    # the next test tries to interact with.
    EMPLOYEE_LIST_HEADER = (By.XPATH, "//h6[contains(., 'Employee Information') or contains(., 'Employee List')]")

    def get_header_title(self) -> str:
        return self.get_text(self.HEADER_TITLE)

    def logout(self):
        self.click(self.USER_DROPDOWN)
        self.click(self.LOGOUT_LINK)
        return self

    def go_to_pim(self):
        self.click(self.PIM_MENU_ITEM)
        # Fail here, clearly, if PIM navigation didn't actually complete —
        # rather than passing silently and leaving every subsequent PIM
        # locator to time out with no indication of the real cause.
        self.find_visible(self.EMPLOYEE_LIST_HEADER, timeout=15)
        return self
