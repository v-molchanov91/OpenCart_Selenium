import pytest
import allure
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


def pytest_addoption(parser):
    parser.addoption('--browser', default='chrome', help='Browser: chrome, firefox, yandex')
    parser.addoption('--browser-version', default='124.0')
    parser.addoption('--yad', default='C:/Users/v.molchanov/Downloads/Drivers/yandexdriver.exe')
    parser.addoption('--remote', action='store_true', help='Run tests on remote Selenoid server')
    parser.addoption('--selenoid-url', default='http://localhost:4444/wd/hub', help='Selenoid URL')
    parser.addoption('--base-url', default='http://192.168.1.19:8081/')


@pytest.fixture(scope='session')
def base_url(pytestconfig):
    return pytestconfig.getoption('base_url')


@pytest.fixture()
def browser(pytestconfig):
    browser_name = pytestconfig.getoption('browser')
    browser_version = pytestconfig.getoption('browser_version')
    yad = pytestconfig.getoption('yad')
    remote = pytestconfig.getoption('remote')
    selenoid_url = pytestconfig.getoption('selenoid_url')

    driver = None

    if browser_name == 'chrome':
        options = ChromeOptions()
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        if remote:
            options.set_capability("browserName", "chrome")
            options.set_capability("browserVersion", browser_version)
            options.set_capability("selenoid:options", {
                "enableVNC": True,
                "enableVideo": False
            })
            driver = webdriver.Remote(
                command_executor=selenoid_url,
                options=options
            )
        else:
            driver = webdriver.Chrome(options=options)

    elif browser_name == 'firefox':
        options = FirefoxOptions()
        if remote:
            options.set_capability("browserName", "firefox")
            options.set_capability("browserVersion", browser_version)
            options.set_capability("selenoid:options", {
                "enableVNC": True,
                "enableVideo": False
            })
            driver = webdriver.Remote(
                command_executor=selenoid_url,
                options=options
            )
        else:
            driver = webdriver.Firefox(options=options)

    elif browser_name == 'yandex':
        if not os.path.exists(yad):
            raise FileNotFoundError(f"Yandex Driver not found at {yad}")
        service = Service(executable_path=yad)
        options = ChromeOptions()
        options.binary_location = "C:/Program Files (x86)/Yandex/YandexBrowser/Application/browser.exe"
        driver = webdriver.Chrome(options=options, service=service)

    else:
        raise ValueError(f"Unsupported browser: {browser_name}")

    yield driver
    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get('browser', None)
        if driver:
            screenshot_path = f"screenshots/{item.name}.png"
            os.makedirs("screenshots", exist_ok=True)
            driver.save_screenshot(screenshot_path)
            allure.attach.file(screenshot_path, name="screenshot", attachment_type=allure.attachment_type.PNG)

        selenoid_url = item.config.getoption("selenoid_url")
        if item.config.getoption("remote"):
            video_url = f"{selenoid_url}/video/{item.name}.mp4"
            allure.attach(video_url, name="Test Video", attachment_type=allure.attachment_type.MP4)
