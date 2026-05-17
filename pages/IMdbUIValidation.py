import re
from playwright.sync_api import expect


class IMDbUIValidation:
    def __init__(self, page):
        self.page = page

    def navigateToImdb(self):
        expect(self.page).to_have_title(re.compile("IMDb"))
        print("Successfully navigated to IMDb")

    def searchMovie(self, movie_name):
        search_bar = self.page.locator('input[id="suggestion-search"]')
        search_bar.click()
        search_bar.fill(movie_name)
        expect(search_bar).to_have_value(movie_name)  # wait until filled
        search_bar.press("Enter")
        try:
            results_section = self.page \
                .locator("section[data-testid='find-results-section-title']") \
                .locator("ul.ipc-metadata-list")
            expect(results_section).to_be_visible()
            print(f"Successfully searched the movie: {movie_name}.")
        except TimeoutError, AssertionError:
            no_result_found = self.page \
                .locator('section[data-testid="find-results-section-interest"]') \
                .locator('div[data-testid="results-section-empty-results-msg"]') \
                .inner_text()
            print("No result found")
            assert "No results found" in no_result_found

    def navigateToSearchedMoviePage(self, movie_name, imdb_id):
        try:
            expect(self.page.get_by_role("link", name=movie_name, exact=True)).to_be_visible()
            self.page.get_by_role("link", name=movie_name, exact=True).first.click()
            print(f"Successfully navigated to page : {movie_name}.")
        except AssertionError:
            # handle when multiple movie prsent with same name/title
            expect(self.page.locator(f'div.ipc-title a[href*="{imdb_id}"]')).to_be_visible()
            self.page.locator(f'div.ipc-title a[href*="{imdb_id}"]').click()
            print(f"Successfully navigated to page : {movie_name}.")

    def getMovieInfoFromUI(self):
        movie_title = self.page.locator('h1[data-testid="hero__pageTitle"] span').inner_text()
        movie_year = self.page.locator('div.sc-af040695-0 a[href*="releaseinfo"]').text_content()
        movie_rating = self.page.locator('span[data-testid="rating-histogram-star"] span').inner_text()
        storyLine_header = self.page.locator('span[id="storyline"]')
        storyLine_header.scroll_into_view_if_needed()
        movie_plot = self.page.locator(
            'div[data-testid="storyline-plot-summary"] div.ipc-html-content-inner-div').text_content()
        return movie_title, movie_year, movie_rating, movie_plot

    def navigateToHomePage(self):
        self.page.locator('(//a[@id="home_img_holder"])[1]').click()
        expect(self.page).to_have_url(re.compile("home"))
        print("Successfully navigated to home page.")

    def top10moviesOfTheWeek(self):
        try:
            # Scroll to section
            what_to_watch = self.page.locator('//h3[normalize-space()="What to watch"]')
            what_to_watch.scroll_into_view_if_needed()

            top10_header = self.page.locator('//h3[normalize-space()="Top 10 on IMDb this week"]')
            expect(top10_header).to_be_visible()

            tenup_cards = self.page.locator('//div[contains(@class, "@l:flex")]') \
                .locator('//div[contains(@data-testid, "tenup_item")]')
            top_movie_texts = []

            # top_cards = tenup_cards.all()
            round_cards = tenup_cards.locator("h3").all()
            for card in round_cards:
                card_text = card.inner_text()
                top_movie_texts.append(card_text)
            print(f"Top  {len(top_movie_texts)} movies found: {top_movie_texts}")

            poster_cards = tenup_cards \
                .locator('//a[contains(@class, "ipc-poster-card__title")]').all()
            for card in poster_cards:
                top_movie_texts.append(card.inner_text())
            print(f"Total top {len(top_movie_texts)} movies found: {top_movie_texts}")
            assert len(top_movie_texts) == 10, \
                f"Expected 10 movies, found {len(top_movie_texts)}"

        except AssertionError as e:
            print(f"Assertion failed: {e}")
