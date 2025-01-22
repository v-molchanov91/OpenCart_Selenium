import allure
from pages.base_page import BasePage
from selenium.webdriver.common.by import By


class MainPage(BasePage):
    CURRENCY_BUTTON = (By.CSS_SELECTOR, "#form-currency .dropdown-toggle")
    EUR_OPTION = (By.CSS_SELECTOR, "a.dropdown-item[href='EUR']")
    PRICE = (By.CSS_SELECTOR, ".price")

    @allure.step("Переключаем валюту на евро")
    def switch_currency_to_euro(self):
        self.logger.info("Переключаем валюту на евро.")
        self.click(*self.CURRENCY_BUTTON)
        self.click(*self.EUR_OPTION)

    @allure.step("Получаем цену товара с текущей валютой")
    def get_price_currency(self):
        self.logger.info("Получаем цену товара.")
        return self.get_text(*self.PRICE)
