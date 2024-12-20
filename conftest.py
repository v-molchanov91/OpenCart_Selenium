import pytest
import allure
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


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    result = outcome.get_result()
    if result.when == "call" and result.failed:
        browser = item.funcargs.get("browser")
        if browser:
            screenshot_path = "screenshot.png"
            browser.save_screenshot(screenshot_path)
            allure.attach.file(screenshot_path, name="Screenshot", attachment_type=allure.attachment_type.PNG)