import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import pytest
import allure
import time
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pages.login_page import LoginPage
from pages.search_page import SearchPage
from config import BASE_URL, SECOND_URL


FAILURE_DIR    = "utilities/screenshots/failures"
CLICK_DIR      = "utilities/screenshots/clicks"
ALLURE_RESULTS = "reports/allure-results"

os.makedirs(FAILURE_DIR, exist_ok=True)
os.makedirs(CLICK_DIR, exist_ok=True)
os.makedirs(ALLURE_RESULTS, exist_ok=True)


def take_failure_screenshot(driver, test_name):
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    path = os.path.join(FAILURE_DIR, f"FAIL_{test_name}_{timestamp}.png")
    driver.save_screenshot(path)
    print(f"\n❌ Failure screenshot: {path}")
    return path


# ── auto open allure report after tests finish ───────────────
def pytest_sessionfinish(session, exitstatus):
    """Automatically opens allure report when all tests are done."""
    print("\n\n📊 Generating Allure Report...")
    subprocess.Popen(
        ["allure", "serve", ALLURE_RESULTS],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    print("✅ Allure report opened in browser!")


# ── driver fixture ───────────────────────────────────────────
@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    yield driver
    driver.quit()


# ── page fixtures ────────────────────────────────────────────
@pytest.fixture(scope="function")
def open_login_page(driver):
    driver.get(BASE_URL)
    return LoginPage(driver)


@pytest.fixture(scope="function")
def open_search_page(driver):
    driver.get(SECOND_URL)
    return SearchPage(driver)


# ── screenshot on failure ────────────────────────────────────
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            screenshot_path = take_failure_screenshot(driver, item.name)

            # attach to allure report
            allure.attach(
                driver.get_screenshot_as_png(),
                name=f"FAIL_{item.name}",
                attachment_type=allure.attachment_type.PNG
            )

            # attach to html report
            from pytest_html import extras
            if not hasattr(report, "extra"):
                report.extra = []
            report.extra.append(extras.image(screenshot_path))