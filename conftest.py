import pytest
from utils.driver_factory import get_driver
from pages.login_page import LoginPage

# OrangeHRM publishes these credentials publicly on their own demo site
# for exactly this purpose (anyone can self-serve a sandbox instance).
VALID_USERNAME = "Admin"
VALID_PASSWORD = "admin123"


@pytest.fixture
def driver():
    drv = get_driver(headless=True)
    yield drv
    drv.quit()


@pytest.fixture
def logged_in_driver(driver):
    """Provides a driver already past login, for tests that only care
    about post-login behavior (PIM, dashboard, etc.).
    """
    LoginPage(driver).load().login(VALID_USERNAME, VALID_PASSWORD)
    return driver
