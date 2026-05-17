import pytest
from playwright.sync_api import Playwright

def pytest_addoption(parser):
    parser.addoption("--browser_name", action="store", default="chrome", help="browser to use")
    parser.addoption("--movie_name", action="store", default="Inception", help="browser to use")


@pytest.fixture(scope="module")
def browser_instance(playwright: Playwright, request):
    global browser
    browser_name = request.config.getoption("--browser_name")
    if browser_name == "chrome":
        browser = playwright.chromium.launch(headless=False)
    elif browser_name == "firefox":
        browser = playwright.firefox.launch(headless=False)
    context = browser.new_context()
    context.tracing.start(screenshots=True, snapshots=True)
    page = context.new_page()
    page.goto("https://www.imdb.com/")
    yield page
    context.tracing.stop(path="trace.zip")
    context.close()
    browser.close()

@pytest.fixture
def movie_mame(request):
    return request.config.getoption("--movie_name")
