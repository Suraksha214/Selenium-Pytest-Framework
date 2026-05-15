from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class LoginPage(BasePage):

    USERNAME = (By.ID, "user-name")
    PASSWORD = (By.ID, "password")
    LOGIN_BTN = (By.ID, "login-button")
    INVENTORY_CONTAINER = (By.ID, "inventory_container")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")  # ← error element on saucedemo

    def __init__(self, driver):
        super().__init__(driver)

    def login(self, username, password):
        self.send_keys(self.USERNAME, username)
        self.send_keys(self.PASSWORD, password)
        self.click(self.LOGIN_BTN)

    def wait_for_dashboard(self):
        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(self.INVENTORY_CONTAINER)
        )

    def wait_for_error(self):
        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(self.ERROR_MESSAGE)
        )