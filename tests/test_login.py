from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

VALID_USERNAME = "Admin"
VALID_PASSWORD = "admin123"


class TestLogin:
    def test_successful_login_lands_on_dashboard(self, driver):
        login_page = LoginPage(driver).load()
        login_page.login(VALID_USERNAME, VALID_PASSWORD)
        dashboard = DashboardPage(driver)
        assert dashboard.get_header_title() == "Dashboard"

    def test_invalid_password_shows_error(self, driver):
        login_page = LoginPage(driver).load()
        login_page.login(VALID_USERNAME, "wrong_password")
        assert "Invalid credentials" in login_page.get_error_message()

    def test_unregistered_username_shows_same_generic_error(self, driver):
        # Same assertion as the wrong-password case is intentional: the
        # app should not reveal whether the username exists.
        login_page = LoginPage(driver).load()
        login_page.login("not_a_real_user", "whatever123")
        assert "Invalid credentials" in login_page.get_error_message()

    def test_empty_username_shows_required_field_error(self, driver):
        login_page = LoginPage(driver).load()
        login_page.login("", VALID_PASSWORD)
        assert "Required" in login_page.get_required_field_error()
