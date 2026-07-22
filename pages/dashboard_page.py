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
    PIM_MENU_ITEM = (By.XPATH, "//span[text()='PIM']")

    def get_header_title(self) -> str:
        return self.get_text(self.HEADER_TITLE)

    def logout(self):
        self.click(self.USER_DROPDOWN)
        self.click(self.LOGOUT_LINK)
        return self

    def go_to_pim(self):
        self.click(self.PIM_MENU_ITEM)
        return self
