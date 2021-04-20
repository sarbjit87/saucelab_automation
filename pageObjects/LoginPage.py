from common.base_page import BasePage
from selenium.webdriver.common.by import By

class LoginPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    # Locators
    user_name = (By.ID, "user-name")
    password = (By.ID, "password")
    login_button = (By.ID, "login-button")
    error_message = (By.CSS_SELECTOR, "[data-test='error']")

    def do_login(self, username, password):
        self.clear(self.user_name)
        self.send_keys(self.user_name, username)
        self.clear(self.password)
        self.send_keys(self.password, password)
        self.press_button(self.login_button)

    def get_error_message(self):
        error = self.get_element_text(self.error_message)
        return error