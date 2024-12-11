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

    def login(self, username, password):
        self.type(*self.USERNAME_INPUT, username)
        self.type(*self.PASSWORD_INPUT, password)
        self.click(*self.LOGIN_BUTTON)

    def logout(self):
        self.click(*self.LOGOUT_BUTTON)

    def open_catalog(self):
        self.click(*self.CATALOG_MENU)
        self.click(*self.PRODUCTS_LINK)

    def add_product(self):
        self.click(*self.ADD_PRODUCT_BUTTON)
        # Add product form logic goes here

    def delete_product(self):
        self.click(*self.DELETE_PRODUCT_BUTTON)
