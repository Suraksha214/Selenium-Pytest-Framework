from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:

    def __init__(self, driver):
        self.driver = driver

    def click(self, locator):
        element = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()

    def send_keys(self, locator, text):
        element = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(locator)
        )
        element.clear()
        element.send_keys(text)

    def safe_click(self, locator):
        element = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()