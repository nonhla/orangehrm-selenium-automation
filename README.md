# orangehrm-selenium-automation

A Selenium + pytest UI automation framework using the **Page Object Model (POM)**, tested against the [OrangeHRM demo site](https://opensource-demo.orangehrmlive.com/web/index.php/auth/login) — a public, self-service HR management app widely used for automation practice.

## Why this project

This covers a **real multi-step workflow** (login → navigate to a module → create/search data), not just a login form. That's a better demonstration of framework design than most portfolio projects, since it forces the Page Object Model to actually earn its keep across pages that depend on each other.

## Why Page Object Model

Scripts that mix Selenium locators directly into test functions break constantly and are painful to maintain. POM separates **page structure** (locators, page actions) from **test logic** (assertions, scenarios), so a UI change means updating one page object, not every test that touches that page.

## Structure

```
orangehrm-selenium-automation/
├── pages/
│   ├── base_page.py         # Shared wait/interaction helpers
│   ├── login_page.py         # Locators + actions for the login page
│   ├── dashboard_page.py      # Post-login navigation (side menu, logout)
│   └── pim_page.py            # Add Employee + Employee Search
├── tests/
│   ├── test_login.py           # Valid login, invalid password, unknown user, empty field
│   ├── test_add_employee.py    # Create a new employee record
│   └── test_employee_search.py # Search with and without results
├── utils/
│   └── driver_factory.py      # Centralized WebDriver setup
├── conftest.py                  # Fixtures, incl. a pre-logged-in driver
├── requirements.txt
└── .github/workflows/tests.yml
```

## Running locally

```bash
pip install -r requirements.txt
pytest -v
```

Runs headless Chrome by default (works in CI with no display). Uses OrangeHRM's publicly published demo credentials (`Admin` / `admin123`) — no real accounts or data involved.

## What this demonstrates

- Page Object Model architecture across multiple, dependent pages
- Explicit waits instead of `time.sleep()` (flaky-test prevention)
- Test isolation strategy for a shared public demo instance (unique data per run so tests don't collide)
- Headless CI execution via GitHub Actions
- Both positive and negative test design (invalid login, empty search results)

## A note on the demo site

OrangeHRM's demo instance is shared publicly, resets periodically, and can be slower or flakier than a real staging environment. The tests are written defensively around that (generous timeouts, unique data per run), which is itself a realistic constraint — production test suites often have to account for shared/unstable environments too.
