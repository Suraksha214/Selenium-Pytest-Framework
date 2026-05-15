from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage


class SearchPage(BasePage):
    SEARCH_BOX = (By.ID, "sb_form_q")  # ← bing search box ID
    RESULTS = (By.ID, "b_results")  # ← google results container

    def __init__(self, driver):
        super().__init__(driver)

    def search(self, keyword):
        self.send_keys(self.SEARCH_BOX, keyword)
        self.driver.find_element(*self.SEARCH_BOX).send_keys(Keys.RETURN)

    def wait_for_results(self):
        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(self.RESULTS)
        )