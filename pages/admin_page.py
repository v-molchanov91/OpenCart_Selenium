import allure
from pages.base_page import BasePage
from selenium.webdriver.common.by import By


class AdminPage(BasePage):
    USERNAME_INPUT = (By.ID, "input-username")
    PASSWORD_INPUT = (By.ID, "input-password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    LOGOUT_BUTTON = (By.XPATH, '//a[span[text()="Logout"]]')
    CATALOG_MENU = (By.XPATH, '//a[contains(text(), "Catalog")]')
    PRODUCTS_LINK = (By.XPATH, '//a[contains(text(), "Products")]')
    ADD_PRODUCT_BUTTON = (By.CSS_SELECTOR, "button[data-original-title='Add New']")
    DELETE_PRODUCT_BUTTON = (By.CSS_SELECTOR, "button[data-original-title='Delete']")
    PRODUCT_NAME_INPUT = (By.ID, "input-name1")
    SAVE_BUTTON = (By.CSS_SELECTOR, "button[data-original-title='Save']")

    @allure.step("Логинимся в админку с логином {username}")
    def login(self, username, password):
        self.logger.info("Авторизация в админке.")
        self.input_text(*self.USERNAME_INPUT, username)
        self.input_text(*self.PASSWORD_INPUT, password)
        self.input_text(*self.LOGIN_BUTTON)

    @allure.step("Выходим из админки")
    def logout(self):
        self.logger.info("Выходим из админки.")
        self.click(*self.LOGOUT_BUTTON)

    @allure.step("Открываем каталог товаров")
    def open_catalog(self):
        self.logger.info("Переходим в раздел каталога товаров.")
        self.click(*self.CATALOG_MENU)
        self.click(*self.PRODUCTS_LINK)

    @allure.step("Добавляем продукт")
    def add_product(self, product_name):
        self.logger.info(f"Добавляем продукт: {product_name}")
        self.click(*self.ADD_PRODUCT_BUTTON)
        self.input_text(*self.PRODUCT_NAME_INPUT, product_name)
        self.click(*self.SAVE_BUTTON)

    @allure.step("Удаляем продукт")
    def delete_product(self):
        self.logger.info("Удаляем продукт.")
        self.click(*self.DELETE_PRODUCT_BUTTON)
