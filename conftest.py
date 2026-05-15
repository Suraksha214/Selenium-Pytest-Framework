import sys
import os
import time
import logging

import pytest
import allure

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pytest_html import extras

from pages.login_page import LoginPage
from pages.search_page import SearchPage
from config import BASE_URL, SECOND_URL


# ─────────────────────────────────────────────────────────────
# Project Path
# ─────────────────────────────────────────────────────────────
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


# ─────────────────────────────────────────────────────────────
# Folders
# ─────────────────────────────────────────────────────────────
FAILURE_DIR = "utilities/screenshots/failures"
CLICK_DIR = "utilities/screenshots/clicks"
ALLURE_RESULTS = "reports/allure-results"

os.makedirs(FAILURE_DIR, exist_ok=True)
os.makedirs(CLICK_DIR, exist_ok=True)
os.makedirs(ALLURE_RESULTS, exist_ok=True)


# ─────────────────────────────────────────────────────────────
# Logging Configuration
# ─────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="framework.log",
    filemode="a"
)

logger = logging.getLogger()


# ─────────────────────────────────────────────────────────────
# Screenshot Utility
# ─────────────────────────────────────────────────────────────
def take_failure_screenshot(driver, test_name):
    timestamp = time.strftime("%Y%m%d_%H%M%S")

    screenshot_path = os.path.join(
        FAILURE_DIR,
        f"FAILED_{test_name}_{timestamp}.png"
    )

    driver.save_screenshot(screenshot_path)

    logger.error(f"Screenshot captured: {screenshot_path}")

    print(f"\n❌ Failure Screenshot Saved: {screenshot_path}")

    return screenshot_path


# ─────────────────────────────────────────────────────────────
# Pytest Session Finish
# ─────────────────────────────────────────────────────────────
def pytest_sessionfinish(session, exitstatus):
    print("\n📊 Allure results generated successfully!")
    logger.info("Test execution completed.")


# ─────────────────────────────────────────────────────────────
# WebDriver Fixture
# ─────────────────────────────────────────────────────────────
@pytest.fixture(scope="function")
def driver():

    logger.info("Launching Chrome Browser")

    chrome_options = webdriver.ChromeOptions()

    chrome_options.add_argument("--start-maximized")

    # Uncomment for headless execution
    # chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

    yield driver

    logger.info("Closing Browser")

    driver.quit()


# ─────────────────────────────────────────────────────────────
# Login Page Fixture
# ─────────────────────────────────────────────────────────────
@pytest.fixture(scope="function")
def open_login_page(driver):

    logger.info(f"Opening Login Page: {BASE_URL}")

    driver.get(BASE_URL)

    return LoginPage(driver)


# ─────────────────────────────────────────────────────────────
# Search Page Fixture
# ─────────────────────────────────────────────────────────────
@pytest.fixture(scope="function")
def open_search_page(driver):

    logger.info(f"Opening Search Page: {SECOND_URL}")

    driver.get(SECOND_URL)

    return SearchPage(driver)


# ─────────────────────────────────────────────────────────────
# Screenshot on Test Failure
# ─────────────────────────────────────────────────────────────
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield

    report = outcome.get_result()

    if report.when == "call" and report.failed:

        logger.error(f"Test Failed: {item.name}")

        driver = item.funcargs.get("driver")

        if driver:

            screenshot_path = take_failure_screenshot(
                driver,
                item.name
            )

            # Attach screenshot to Allure Report
            allure.attach(
                driver.get_screenshot_as_png(),
                name=f"FAILED_{item.name}",
                attachment_type=allure.attachment_type.PNG
            )

            # Attach screenshot to HTML Report
            if not hasattr(report, "extra"):
                report.extra = []

            report.extra.append(
                extras.image(screenshot_path)
            )