import allure
from pages.admin_page import AdminPage
from pages.main_page import MainPage
from pages.registration_page import RegistrationPage


@allure.title("Тест входа и выхода из админки")
@allure.description("Проверяем успешный вход в админку и выход из нее")
def test_admin_login_logout(browser):
    admin_page = AdminPage(browser)
    admin_page.login("user", "bitnami")
    assert admin_page.find(*AdminPage.LOGOUT_BUTTON), "Кнопка выхода не найдена!"
    admin_page.logout()
    assert admin_page.find(*AdminPage.USERNAME_INPUT), "Поле ввода логина не найдено!"


@allure.title("Тест добавления и удаления продукта")
@allure.description("Проверяем добавление и удаление товара в админке")
def test_add_and_delete_product(browser):
    admin_page = AdminPage(browser)
    admin_page.login("user", "bitnami")
    admin_page.open_catalog()
    admin_page.add_product()
    admin_page.delete_product()


@allure.title("Тест переключения валюты на главной странице")
@allure.description("Проверяем переключение валюты на евро")
def test_currency_switch(browser):
    main_page = MainPage(browser)
    main_page.switch_currency_to_euro()
    price = main_page.get_price_currency()
    assert "€" in price, "Цена не отображается в евро!"


@allure.title("Тест регистрации пользователя")
@allure.description("Регистрируем пользователя с указанными данными")
def test_user_registration(browser):
    registration_page = RegistrationPage(browser)
    registration_page.register_user("John", "Doe", "john.doe@example.com", "password123")
    assert registration_page.check_successful_registration(), "Регистрация неуспешна!"






