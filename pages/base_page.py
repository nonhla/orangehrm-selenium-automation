from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    """Shared functionality for all page objects.

    Every page object inherits from this so wait/interaction logic lives in
    one place instead of being copy-pasted across pages.
    """

    DEFAULT_TIMEOUT = 10

    def __init__(self, driver):
        self.driver = driver

    def find(self, locator, timeout=DEFAULT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

    def find_visible(self, locator, timeout=DEFAULT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def click(self, locator, timeout=DEFAULT_TIMEOUT):
        element = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()

    def type_text(self, locator, text, timeout=DEFAULT_TIMEOUT):
        element = self.find_visible(locator, timeout)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator, timeout=DEFAULT_TIMEOUT):
        return self.find_visible(locator, timeout).text
