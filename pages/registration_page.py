import allure
from pages.base_page import BasePage
from selenium.webdriver.common.by import By


class RegistrationPage(BasePage):
    FIRSTNAME_INPUT = (By.ID, "input-firstname")
    LASTNAME_INPUT = (By.ID, "input-lastname")
    EMAIL_INPUT = (By.ID, "input-email")
    PASSWORD_INPUT = (By.ID, "input-password")
    CONTINUE_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".alert-success")

    @allure.step("Регистрируем пользователя: {firstname} {lastname}")
    def register_user(self, firstname, lastname, email, password):
        self.logger.info(f"Регистрируем пользователя: {firstname} {lastname}, Email: {email}")
        self.input_text(*self.FIRSTNAME_INPUT, firstname)
        self.input_text(*self.LASTNAME_INPUT, lastname)
        self.input_text(*self.EMAIL_INPUT, email)
        self.input_text(*self.PASSWORD_INPUT, password)
        self.input_text(*self.CONTINUE_BUTTON)

    @allure.step("Проверяем успешную регистрацию")
    def check_successful_registration(self):
        self.logger.info("Проверяем наличие сообщения об успешной регистрации.")
        return self.find(*self.SUCCESS_MESSAGE)
