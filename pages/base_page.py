from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, browser):
        self.browser = browser
        self.wait = WebDriverWait(browser, 10)

    def find(self, by, locator):
        return self.wait.until(EC.presence_of_element_located((by, locator)))

    def click(self, by, locator):
        element = self.find(by, locator)
        element.click()

    def type(self, by, locator, text):
        element = self.find(by, locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, by, locator):
        element = self.find(by, locator)
        return element.text
