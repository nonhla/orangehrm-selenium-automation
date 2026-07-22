from pages.dashboard_page import DashboardPage
from pages.pim_page import PimPage


class TestEmployeeSearch:
    def test_search_by_existing_employee_returns_at_least_one_result(self, logged_in_driver):
        # OrangeHRM's demo instance ships with seeded employee data, so a
        # common name is a reasonable positive-path check without needing
        # to create data first.
        DashboardPage(logged_in_driver).go_to_pim()
        pim_page = PimPage(logged_in_driver)
        pim_page.search_employee_by_name("Alice")
        assert pim_page.get_result_row_count() >= 1

    def test_search_by_nonexistent_name_returns_no_results(self, logged_in_driver):
        DashboardPage(logged_in_driver).go_to_pim()
        pim_page = PimPage(logged_in_driver)
        pim_page.search_employee_by_name("Zzzznonexistentname")
        assert pim_page.get_result_row_count() == 0
