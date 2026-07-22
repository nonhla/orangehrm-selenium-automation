from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def get_driver(headless: bool = True):
    """Centralized WebDriver creation so browser config lives in one place."""
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    return webdriver.Chrome(options=options)
