import pytest
import allure
import time
from config import VALID_USER, INVALID_USER, SEARCH_KEYWORD


@allure.feature("Login Functionality")          # ← feature name
class TestLoginRegression:

    @allure.story("Valid Login")                # ← test story
    @allure.severity(allure.severity_level.CRITICAL)
    def test_valid_login(self, open_login_page):
        """TC001 - Valid user should land on inventory page."""
        with allure.step("Enter valid username and password"):
            open_login_page.login(VALID_USER["username"], VALID_USER["password"])
        with allure.step("Wait for dashboard to load"):
            open_login_page.wait_for_dashboard()
        with allure.step("Verify inventory page URL"):
            assert "inventory" in open_login_page.driver.current_url
        time.sleep(2)

    @allure.story("Invalid Login")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_invalid_login(self, open_login_page):
        """TC002 - Invalid user should see error."""
        with allure.step("Enter invalid username and password"):
            open_login_page.login(INVALID_USER["username"], INVALID_USER["password"])
        with allure.step("Wait for error message"):
            open_login_page.wait_for_error()
        with allure.step("Verify still on login page"):
            assert "saucedemo.com" in open_login_page.driver.current_url
        time.sleep(2)

    @allure.story("Empty Username")
    @allure.severity(allure.severity_level.NORMAL)
    def test_empty_username(self, open_login_page):
        """TC003 - Empty username should show error."""
        with allure.step("Enter empty username"):
            open_login_page.login("", VALID_USER["password"])
        with allure.step("Wait for error message"):
            open_login_page.wait_for_error()
        with allure.step("Verify still on login page"):
            assert "saucedemo.com" in open_login_page.driver.current_url
        time.sleep(2)

    @allure.story("Empty Password")
    @allure.severity(allure.severity_level.NORMAL)
    def test_empty_password(self, open_login_page):
        """TC004 - Empty password should show error."""
        with allure.step("Enter empty password"):
            open_login_page.login(VALID_USER["username"], "")
        with allure.step("Wait for error message"):
            open_login_page.wait_for_error()
        with allure.step("Verify still on login page"):
            assert "saucedemo.com" in open_login_page.driver.current_url
        time.sleep(2)

    @allure.story("Empty Credentials")
    @allure.severity(allure.severity_level.MINOR)
    def test_empty_credentials(self, open_login_page):
        """TC005 - Both fields empty should show error."""
        with allure.step("Leave both fields empty"):
            open_login_page.login("", "")
        with allure.step("Wait for error message"):
            open_login_page.wait_for_error()
        with allure.step("Verify still on login page"):
            assert "saucedemo.com" in open_login_page.driver.current_url
        time.sleep(2)


@allure.feature("Search Functionality")         # ← feature name
class TestSearchRegression:

    @allure.story("Valid Search")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_valid_search(self, open_search_page):
        """TC006 - Valid keyword should return results."""
        with allure.step(f"Search for keyword: {SEARCH_KEYWORD}"):
            open_search_page.search(SEARCH_KEYWORD)
        with allure.step("Wait for results to load"):
            open_search_page.wait_for_results()
        with allure.step("Verify results page title"):
            assert "Selenium" in open_search_page.driver.title
        time.sleep(2)

    @allure.story("Different Keyword Search")
    @allure.severity(allure.severity_level.NORMAL)
    def test_different_keyword(self, open_search_page):
        """TC007 - Different keyword should return results."""
        with allure.step("Search for Python automation"):
            open_search_page.search("Python automation")
        with allure.step("Wait for results"):
            open_search_page.wait_for_results()
        with allure.step("Verify results page"):
            assert "Search" in open_search_page.driver.title
        time.sleep(2)

    @allure.story("Numeric Search")
    @allure.severity(allure.severity_level.MINOR)
    def test_numeric_search(self, open_search_page):
        """TC008 - Numeric keyword should return results."""
        with allure.step("Search for numeric keyword"):
            open_search_page.search("12345")
        with allure.step("Wait for results"):
            open_search_page.wait_for_results()
        with allure.step("Verify results page"):
            assert "Search" in open_search_page.driver.title
        time.sleep(2)

    @allure.story("Special Characters Search")
    @allure.severity(allure.severity_level.MINOR)
    def test_special_characters_search(self, open_search_page):
        """TC009 - Special characters should not crash."""
        with allure.step("Search for special characters"):
            open_search_page.search("@#$%")
        with allure.step("Wait for results"):
            open_search_page.wait_for_results()
        with allure.step("Verify results page"):
            assert "Search" in open_search_page.driver.title
        time.sleep(2)