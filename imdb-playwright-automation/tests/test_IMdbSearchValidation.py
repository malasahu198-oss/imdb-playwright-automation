from playwright.sync_api import Playwright, expect

from IMdbValidation.pages.OMdbAPIValidation import OMdbAPIUtils


def test_e2e_IMdbsearchvalidation(playwright: Playwright):
    browserContext = playwright.chromium.launch(headless=False)
    context = browserContext.new_context()
    page = context.new_page()

    omdb_api_object = OMdbAPIUtils()
    rearch_api_data = omdb_api_object.search_Movie(playwright)

    title_api_data = omdb_api_object.getByTitle(playwright)

    # search movie name in IMDB
    movie_name = "The Crack: Inception"
    page.goto("https://www.imdb.com/")
    search_bar = page.locator('input[id="suggestion-search"]')
    search_bar.click()
    search_bar.fill(movie_name)
    page.locator("#suggestion-search-button").click()
    expect(page.locator("section.ipc-page-section--base h1")).to_be_visible()

    # open the search movie name
    # expect(page.locator("div.ipc-title--base a h3.ipc-title__text", has_text=movie_name)).to_be_visible()
    expect(page.get_by_role("link", name=movie_name, exact=True)).to_be_visible()
    page.get_by_role("link", name=movie_name, exact=True).first.click()

    # extract the movie information
    expect(page.locator('h1[data-testid="hero__pageTitle"] span')).to_contain_text(rearch_api_data["title"])
    expect(page.locator('div.sc-af040695-0 a[href*="releaseinfo"]')).to_contain_text(rearch_api_data["year"])
    expect(page.locator('span[data-testid="rating-histogram-star"] span')).to_contain_text(title_api_data["rating"])
    storyLine_header = page.locator('span[id="storyline"]')
    storyLine_header.scroll_into_view_if_needed()
    expect(page.locator('div[data-testid="storyline-plot-summary"] div.ipc-html-content-inner-div')).to_contain_text(
        title_api_data["plot"])

