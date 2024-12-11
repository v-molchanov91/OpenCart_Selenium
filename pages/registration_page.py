from pages.base_page import BasePage
from selenium.webdriver.common.by import By


class RegistrationPage(BasePage):
    FIRSTNAME_INPUT = (By.ID, "input-firstname")
    LASTNAME_INPUT = (By.ID, "input-lastname")
    EMAIL_INPUT = (By.ID, "input-email")
    PASSWORD_INPUT = (By.ID, "input-password")
    CONTINUE_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")

    def register_user(self, firstname, lastname, email, password):
        self.type(*self.FIRSTNAME_INPUT, firstname)
        self.type(*self.LASTNAME_INPUT, lastname)
        self.type(*self.EMAIL_INPUT, email)
        self.type(*self.PASSWORD_INPUT, password)
        self.click(*self.CONTINUE_BUTTON)
