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
        # EC.element_to_be_clickable(locator) only ever inspects the FIRST
        # element matching the locator. Responsive UIs commonly render a
        # second, hidden copy of the same button (e.g. a mobile-layout
        # duplicate) earlier in the DOM — if that hidden one happens to be
        # the first match, the wait times out even though a perfectly
        # clickable visible copy exists later on the page. Polling across
        # ALL matches for the first visible+enabled one avoids that trap.
        def _first_clickable(driver):
            for element in driver.find_elements(*locator):
                try:
                    if element.is_displayed() and element.is_enabled():
                        return element
                except Exception:
                    continue
            return False

        element = WebDriverWait(self.driver, timeout).until(_first_clickable)
        element.click()

    def type_text(self, locator, text, timeout=DEFAULT_TIMEOUT):
        element = self.find_visible(locator, timeout)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator, timeout=DEFAULT_TIMEOUT):
        return self.find_visible(locator, timeout).text

    def get_nonblank_text(self, locator, timeout=DEFAULT_TIMEOUT):
        """Like get_text, but waits for the text to actually be populated.

        In a reactive SPA like OrangeHRM's, an element can become visible
        in the DOM before its content has finished loading from a
        follow-up API call — the URL changes, the heading element exists
        and is visible, but its text is still blank for a moment. A plain
        visibility wait doesn't catch that; this does.
        """
        def _has_text(driver):
            elements = driver.find_elements(*locator)
            if not elements:
                return False
            text = elements[0].text.strip()
            return text if text else False

        return WebDriverWait(self.driver, timeout).until(_has_text)
