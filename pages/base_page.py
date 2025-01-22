import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException


class BasePage:
    def __init__(self, browser, base_url=""):
        self.browser = browser
        self.base_url = base_url
        self.wait = WebDriverWait(browser, 10)
        self.logger = logging.getLogger(self.__class__.__name__)

    def open(self, url=""):
        full_url = f"{self.base_url}{url}" if self.base_url and not url.startswith("http") else url
        self.logger.info(f"Открываем URL: {full_url}")
        self.browser.get(full_url)

    def find(self, by, locator):
        try:
            self.logger.info(f"Ищем элемент {locator}")
            return self.wait.until(EC.presence_of_element_located((by, locator)))
        except TimeoutException:
            self.logger.error(f"Элемент {locator} не найден в течение заданного времени!")
            raise

    def click(self, by, locator):
        try:
           self.logger.info(f"Кликаем на элемент {locator}")
           element = self.find(by, locator)
           element.click()
        except WebDriverException as e:
            self.logger.error(f"Ошибка при попытке кликнуть на элемент {locator}: {e}")
            raise

    def input_text(self, by, locator, text):
        try:
            self.logger.info(f"Вводим текст '{text}' в элемент {locator}")
            element = self.find(by, locator)
            element.clear()
            element.send_keys(text)
        except WebDriverException as e:
            self.logger.error(f"Ошибка при вводе текста в элемент {locator}: {e}")
            raise

    def get_text(self, by, locator):
        try:
            self.logger.info(f"Получаем текст элемента {locator}")
            element = self.find(by, locator)
            return element.text
        except WebDriverException as e:
            self.logger.error(f"Ошибка при получении текста элемента {locator}: {e}")
            raise
