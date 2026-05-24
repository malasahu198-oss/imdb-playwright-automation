# File: /Users/malasahu098/PycharmProjects/PythonProject/imdb-playwright-automation/pages/BasePage.py

import logging
from playwright.sync_api import Page

logger = logging.getLogger(__name__)


class BasePage:

    def __init__(self, page: Page):
        self.page = page
        self.logger = logger

    def wait_for_page_load(self, timeout: int = 10000) -> None:
        """Wait for page to fully load"""
        self.page.wait_for_load_state("networkidle", timeout=timeout)
        self.logger.info("Page loaded successfully")

    def navigate_to_url(self, url: str) -> None:
        """Navigate to a specific URL"""
        self.page.goto(url)
        self.logger.info(f"Navigated to {url}")

    def wait_for_element(self, locator: str, timeout: int = 5000) -> bool:
        """Wait for element visibility"""
        try:
            self.page.locator(locator).wait_for(timeout=timeout)
            return True
        except:
            self.logger.warning(f"Element not found: {locator}")
            return False

    def scroll_to_element(self, locator: str) -> None:
        """Scroll element into view"""
        self.page.locator(locator).scroll_into_view_if_needed()
