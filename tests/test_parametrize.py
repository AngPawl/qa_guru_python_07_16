import pytest
from selenium.webdriver.chrome.options import Options
from selene import browser, have

"""
Переопределите параметр с помощью indirect параметризации на уровне теста
"""


@pytest.fixture(params=['1920,1080', '1366,768', '400,493'])
def setup_browser(request):
    options = Options()
    options.add_argument(f"window-size={request.param}")
    browser.config.driver_options = options
    browser.config.base_url = 'https://github.com'

    yield

    browser.quit()


desktop_only = pytest.mark.parametrize(
    'setup_browser', ['1920,1080', '1366,768'], indirect=True
)
mobile_only = pytest.mark.parametrize('setup_browser', ['400,493'], indirect=True)


@desktop_only
def test_github_desktop(setup_browser):
    browser.open('/')

    browser.element('[class*=--sign-in]').click()

    browser.element('.auth-form-header h1').should(have.exact_text('Sign in to GitHub'))


@mobile_only
def test_github_mobile(setup_browser):
    browser.open('/')

    browser.element('.Button--link').click()
    browser.element('[class*=--sign-in]').click()

    browser.element('.auth-form-header h1').should(have.exact_text('Sign in to GitHub'))
