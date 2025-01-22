def test_check_title(browser, base_url):
    browser.get(base_url)
    assert 'Your Store' in browser.title, 'Тайтл отличается от ожидаемого'


def test_check_title_login(browser, base_url):
    browser.get(f'{base_url}/administration')
    assert 'Administration' in browser.title, 'Тайтл отличается от ожидаемого'



