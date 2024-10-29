def test_check_title(browser):
    browser.get(browser.base_url)
    assert 'Your Store' in browser.title, 'Тайтл отличается от ожидаемого'


def test_check_title_login(browser):
    browser.get(f'{browser.base_url}/administration')
    assert 'Administration' in browser.title, 'Тайтл отличается от ожидаемого'



