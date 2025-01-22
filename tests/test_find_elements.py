import time

import allure
from pages.admin_page import AdminPage
from pages.main_page import MainPage
from pages.registration_page import RegistrationPage


@allure.title("Тест входа и выхода из админки")
@allure.description("Проверяем успешный вход в админку и выход из нее")
def test_admin_login_logout(browser, base_url):
    admin_page = AdminPage(browser)
    admin_page.open(f"{base_url}/administration")
    admin_page.login("user", "bitnami")
    assert admin_page.find(*AdminPage.LOGOUT_BUTTON), "Кнопка выхода не найдена!"
    admin_page.logout()
    assert admin_page.find(*AdminPage.USERNAME_INPUT), "Поле ввода логина не найдено!"


@allure.title("Тест добавления и удаления продукта")
@allure.description("Проверяем добавление и удаление товара в админке")
def test_add_and_delete_product(browser, base_url):
    admin_page = AdminPage(browser)
    admin_page.open(f"{base_url}/administration")
    admin_page.login("user", "bitnami")
    admin_page.open_catalog()
    admin_page.add_product()
    admin_page.delete_product()


@allure.title("Тест переключения валюты на главной странице")
@allure.description("Проверяем переключение валюты на евро")
def test_currency_switch(browser, base_url):
    main_page = MainPage(browser)
    main_page.open(base_url)
    initial_price = main_page.get_price_currency()
    main_page.switch_currency_to_euro()
    updated_price = main_page.get_price_currency()
    assert "€" in updated_price, "Цена не отображается в евро!"
    assert initial_price != updated_price, "Цена не изменилась после переключения валюты!"


@allure.title("Тест регистрации пользователя")
@allure.description("Регистрируем пользователя с указанными данными")
def test_user_registration(browser, base_url):
    registration_page = RegistrationPage(browser)
    registration_page.open(f'{base_url}/en-gb?route=account/register')
    registration_page.register_user("John", "Doe", "john112.droe@example.com", "password123")
    time.sleep(3)
    assert 'Your Account Has Been Created!' in browser.title






