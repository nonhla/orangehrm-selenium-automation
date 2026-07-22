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


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Captures a screenshot on test failure and attaches it to the
    HTML report. This is what real Selenium frameworks do instead of
    debugging blind from a text traceback alone — the screenshot shows
    exactly what the browser saw at the moment of failure (a login wall,
    an unexpected error banner, a slow-loading spinner, etc.).
    """
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver") or item.funcargs.get("logged_in_driver")
        if driver is not None:
            try:
                from pytest_html import extras
                screenshot_b64 = driver.get_screenshot_as_base64()
                extra.append(extras.image(screenshot_b64, mime_type="image/png"))
            except Exception:
                # Never let screenshot capture itself break the test run.
                pass

    report.extra = extra
