import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException


class BasePage:
    def __init__(self, browser):
        self.browser = browser
        self.wait = WebDriverWait(browser, 10)
        self.logger = logging.getLogger(self.__class__.__name__)
        handler = logging.FileHandler("test.log")
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

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
