import pytest
from playwright.sync_api import Playwright


@pytest.fixture(scope="module")
def browser_instance(playwright: Playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.imdb.com/")
    yield page
    context.close()
    browser.close()
