from pages.base_page import BasePage
from selenium.webdriver.common.by import By


class MainPage(BasePage):
    CURRENCY_BUTTON = (By.CSS_SELECTOR, "#form-currency .dropdown-toggle")
    EUR_OPTION = (By.CSS_SELECTOR, "a.dropdown-item[href='EUR']")
    PRICE = (By.CSS_SELECTOR, ".price")

    def switch_currency_to_euro(self):
        self.click(*self.CURRENCY_BUTTON)
        self.click(*self.EUR_OPTION)

    def get_price_currency(self):
        return self.get_text(*self.PRICE)