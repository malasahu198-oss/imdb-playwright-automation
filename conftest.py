import os

import pytest
from playwright.sync_api import Playwright

def pytest_addoption(parser):
    parser.addoption("--browser_name", action="store", default="chrome", help="browser to use")
    parser.addoption("--movie_name", action="store", default="Inception", help="browser to use")


@pytest.fixture(scope="module")
def browser_instance(playwright: Playwright, request):

    #Auto detect Jenkins — no extra flag needed!
    is_ci = os.getenv("CI") == "true"
    print(f"Running headless: {is_ci}")
    browser_name = request.config.getoption("--browser_name")
    if browser_name == "chrome":
        browser = playwright.chromium.launch(headless=is_ci)
    elif browser_name == "firefox":
        browser = playwright.firefox.launch(headless=is_ci)
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
