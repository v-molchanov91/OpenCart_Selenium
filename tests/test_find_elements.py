import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.admin_page import AdminPage
from pages.main_page import MainPage
from pages.registration_page import RegistrationPage


def test_admin_login_logout(browser):
    admin_page = AdminPage(browser)
    admin_page.login("user", "bitnami")
    assert admin_page.find(*AdminPage.LOGOUT_BUTTON)
    admin_page.logout()
    assert admin_page.find(*AdminPage.USERNAME_INPUT)


def test_add_and_delete_product(browser):
    admin_page = AdminPage(browser)
    admin_page.login("user", "bitnami")
    admin_page.open_catalog()
    admin_page.add_product()
    # Add assertions for product addition
    admin_page.delete_product()
    # Add assertions for product deletion


def test_currency_switch(browser):
    main_page = MainPage(browser)
    main_page.switch_currency_to_euro()
    price = main_page.get_price_currency()
    assert "€" in price


def test_user_registration(browser):
    registration_page = RegistrationPage(browser)
    registration_page.register_user("John", "Doe", "john.doe@example.com", "password123")
    # Add assertions for successful registration






