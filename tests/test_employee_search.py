import time
from pages.dashboard_page import DashboardPage
from pages.pim_page import PimPage


class TestEmployeeSearch:
    def test_search_by_existing_employee_returns_at_least_one_result(self, logged_in_driver):
        # Create the employee first rather than assuming a specific name
        # already exists in the shared demo instance's seed data — the
        # data OrangeHRM ships changes over time, but data we just created
        # ourselves is guaranteed to be there.
        unique_last_name = f"Searchable{int(time.time())}"

        DashboardPage(logged_in_driver).go_to_pim()
        pim_page = PimPage(logged_in_driver)
        pim_page.click_add_employee()
        pim_page.add_employee("Jordan", unique_last_name)
        # Wait for the creation to actually complete before navigating away
        # to search — otherwise this test can race the save request.
        pim_page.get_employee_full_name()

        DashboardPage(logged_in_driver).go_to_pim()
        pim_page.search_employee_by_name(f"Jordan {unique_last_name}")
        assert pim_page.get_result_row_count() >= 1

    def test_search_by_nonexistent_name_returns_no_results(self, logged_in_driver):
        DashboardPage(logged_in_driver).go_to_pim()
        pim_page = PimPage(logged_in_driver)
        pim_page.search_employee_by_name("Zzzznonexistentname")
        assert pim_page.get_result_row_count() == 0
