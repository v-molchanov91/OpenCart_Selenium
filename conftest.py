import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions


def pytest_addoption(parser):
    parser.addoption('--browser', default='chrome')
    parser.addoption('--yad', default='C:/Users/v.molchanov/Downloads/Drivers/yandexdriver.exe')
    parser.addoption('--base-url', default='http://192.168.1.19:8081/')


@pytest.fixture()
def browser(pytestconfig):
    browser_name = pytestconfig.getoption('browser')
    yad = pytestconfig.getoption('yad')
    base_url = pytestconfig.getoption('base_url')
    driver = None

    if browser_name in ['ch', 'chrome']:
        driver = webdriver.Chrome()
    elif browser_name in ['ff', 'firefox']:
        driver = webdriver.Firefox()
    elif browser_name in ['ya', 'yandex']:
        service = Service(executable_path=yad)
        options = ChromeOptions()
        options.binary_location = "C:/Program Files (x86)/Yandex/YandexBrowser/Application/browser.exe"
        driver = webdriver.Chrome(options=options, service=service)

    driver.base_url = base_url
    yield driver
    driver.quit()
