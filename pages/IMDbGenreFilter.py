import logging
from playwright.sync_api import Page, expect
import re

logger = logging.getLogger(__name__)


class IMDbGenreFilter:
    """Page Object for IMDb Advanced Search and Genre Filtering"""

    # Locators (Centralized)
    ALL_FILTER_BUTTON = 'label[data-testid="category-selector-button"] svg'
    SEARCH_CATEGORY_DROPDOWN = 'div[data-menu-id="navbar-search-category-select"] ul'
    ADVANCED_SEARCH_LINK = 'a[href*="hm_nv_srb_menu_adv"]'
    GENRE_DROPDOWN = 'label[aria-label="Collapse Genre"]'
    SEE_RESULTS_BTN = 'button[aria-label="See results"]'
    RESULTS_SECTION = 'ul.ipc-metadata-list'
    RESULT_ITEMS = 'li.ipc-metadata-list-summary-item'

    def __init__(self, page: Page):
        self.page = page

    def _handle_coachmark_and_close(self):
        coachmark = self.page.locator('.navbar__coachmark--fade-in')

        try:
            coachmark.wait_for(state="visible", timeout=5000)
            logger.info("Coachmark appeared — closing it!")
            coachmark.locator('button[title="Close"]').click()
            logger.info("Coachmark closed!")
        except TimeoutError:
            logger.info("Coachmark did not appear — skipping!")

    # UI Actions (No Assertions)
    def navigate_to_advanced_search(self) -> None:
        """Navigate to Advanced Search page"""
        try:
            self._handle_coachmark_and_close()
            all_button = self.page.locator(self.ALL_FILTER_BUTTON)
            all_button.wait_for(timeout=5000)
            all_button.click()
            logger.info("Clicked All Filter Button")
            expect(self.page.locator(self.SEARCH_CATEGORY_DROPDOWN)).to_be_visible()
            self.page.locator(self.ADVANCED_SEARCH_LINK).click()
            logger.info(f"Clicked on the Advanced Search Link")
            self.page.wait_for_url("**hm_nv_srb_menu_adv**")
        except:
            self.page.goto("https://www.imdb.com/search/title/")
            raise
        logger.info("Navigated to Advanced Search")

    def select_genre(self, genre_name: str) -> None:
        """Select a genre from filter dropdown"""
        expect(self.page.locator(self.GENRE_DROPDOWN)).to_have_attribute("aria-expanded", "true")
        self.page.locator(f'//span[contains(text(), "{genre_name}")]').click()
        logger.info(f"Selected genre: {genre_name}")

    def apply_filters(self) -> None:
        """Apply filters and wait for results"""
        self.page.locator(self.SEE_RESULTS_BTN).click()
        self.page.locator(self.RESULTS_SECTION).wait_for(timeout=10000)
        logger.info("Filters applied")

    def get_filtered_results_count(self) -> int:
        """Get count of filtered results"""
        results = self.page.locator(self.RESULT_ITEMS).all()
        return len(results)

    def is_results_loaded(self) -> bool:
        """Check if results section is visible"""
        try:
            self.page.locator(self.RESULTS_SECTION).wait_for(timeout=5000)
            self.page.wait_for_url("**genres=action**")
            return True
        except:
            return False
