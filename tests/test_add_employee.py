import time
from pages.dashboard_page import DashboardPage
from pages.pim_page import PimPage


class TestAddEmployee:
    def test_add_employee_shows_confirmation_with_correct_name(self, logged_in_driver):
        # Unique-ish last name so this test doesn't collide with data
        # left behind by a previous run against the shared demo instance.
        unique_last_name = f"Doe{int(time.time())}"

        DashboardPage(logged_in_driver).go_to_pim()
        pim_page = PimPage(logged_in_driver)
        pim_page.click_add_employee()
        pim_page.add_employee("Jane", unique_last_name)

        full_name = pim_page.get_employee_full_name()
        assert "Jane" in full_name
        assert unique_last_name in full_name
