import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_login_admin_page_elements(browser):
    browser.get(browser.base_url + "/administration")
    wait = WebDriverWait(browser, 10)
    assert wait.until(EC.presence_of_element_located((By.ID, "input-username")))
    assert wait.until(EC.presence_of_element_located((By.ID, "input-password")))
    assert wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit']")))
    assert wait.until(EC.presence_of_element_located((By.XPATH, "//*[text()='OpenCart']")))


def test_main_page(browser):
    browser.get(browser.base_url)
    wait = WebDriverWait(browser, 10)
    assert wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#logo")))
    assert wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".carousel-item")))
    assert wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".navbar")))
    assert wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#search")))
    assert wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a > img[title='iPhone']")))


def test_catalog_page_elements(browser):
    browser.get(browser.base_url + "index.php?route=product/category&path=20")
    wait = WebDriverWait(browser, 10)
    assert wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="product-list"]')))
    assert wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".breadcrumb")))
    assert wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='compare-total']")))
    assert wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".input-group .form-control")))
    assert wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".list-group")))


def test_product_page_elemets(browser):
    browser.get(browser.base_url +"index.php?route=product/product&product_id=40")
    wait = WebDriverWait(browser, 10)
    assert wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='button-group']/button[@title='Add to Wish List']")))
    assert wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#button-cart")))
    assert wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".price")))
    assert wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#tab-description")))
    assert wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".rating")))


def test_registration_page_elements(browser):
    browser.get(browser.base_url + "index.php?route=account/register")
    wait = WebDriverWait(browser, 10)
    assert wait.until(EC.presence_of_element_located((By.ID, "input-firstname")))
    assert wait.until(EC.presence_of_element_located((By.ID, "input-lastname")))
    assert wait.until(EC.presence_of_element_located((By.ID, "input-email")))
    assert wait.until(EC.presence_of_element_located((By.ID, "input-password")))
    assert wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit']")))


def test_admin_login(browser):
    browser.get(browser.base_url + "/administration")
    wait = WebDriverWait(browser, 10)
    browser.find_element(By.XPATH, "//*[@id='input-username']").send_keys("user")
    browser.find_element(By.XPATH, "//*[@id='input-password']").send_keys("bitnami")
    browser.find_element(By.XPATH, '//button[contains(text(), "Login")]').click()
    assert wait.until(EC.presence_of_element_located((By.XPATH, '//a[span[text()="Logout"]]')))
    # Logout
    browser.find_element(By.XPATH, '//a[span[text()="Logout"]]').click()
    assert wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='input-username']")))


def test_add_to_cart(browser):
    browser.get(browser.base_url)
    time.sleep(5)
    add_to_cart_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//div[@class='product-thumb' and .//img[@alt='MacBook']]//button[@aria-label='Add to Cart']")))
    add_to_cart_button.click()
    cart = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'dropdown-toggle')]")))
    assert "1 item(s)" in cart.text


def test_currency_switch(browser):
    browser.get(browser.base_url)
    currency_button = browser.find_element(By.CSS_SELECTOR, "#form-currency .dropdown-toggle")
    currency_button.click()
    browser.find_element(By.CSS_SELECTOR, "a.dropdown-item[href='EUR']").click()
    product_price = browser.find_element(By.CSS_SELECTOR, ".price")
    assert "€" in product_price.text


def test_currency_switch_catalog(browser):
    browser.get(browser.base_url + "index.php?route=product/category&path=20")
    currency_button = browser.find_element(By.CSS_SELECTOR, "#form-currency .dropdown-toggle")
    currency_button.click()
    browser.find_element(By.CSS_SELECTOR, "a.dropdown-item[href='EUR']").click()
    product_price = browser.find_element(By.CSS_SELECTOR, ".price")
    assert "€" in product_price.text




