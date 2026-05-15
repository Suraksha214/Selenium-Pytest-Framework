from config import VALID_USER, INVALID_USER, SEARCH_KEYWORD
import time


class TestFirstSite:

    def test_valid_login(self, open_login_page):
        open_login_page.login(VALID_USER["username"], VALID_USER["password"])
        open_login_page.wait_for_dashboard()
        assert "inventory" in open_login_page.driver.current_url
        time.sleep(3)

    def test_invalid_login(self, open_login_page):
        open_login_page.login(INVALID_USER["username"], INVALID_USER["password"])
        open_login_page.wait_for_error()
        assert "saucedemo.com" in open_login_page.driver.current_url
        time.sleep(3)


class TestSecondSite:

        def test_bing_search(self, open_search_page):
            open_search_page.search(SEARCH_KEYWORD)  # ← types keyword and presses Enter
            open_search_page.wait_for_results()  # ← waits for results page
            assert "Selenium" in open_search_page.driver.title
            assert "Search" in open_search_page.driver.title
            time.sleep(3)  # ← pause to see results