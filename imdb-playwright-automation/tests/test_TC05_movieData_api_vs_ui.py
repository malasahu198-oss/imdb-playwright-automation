from playwright.sync_api import Playwright, expect

from pages.IMdbUIValidation import IMDbUIValidation
from pages.OMdbAPIValidation import OMdbAPIUtils


def test_e2e_IMdbsearchvalidation(playwright: Playwright, browser_instance):
    movie_name = "The Crack: Inception"
    omdb_api_object = OMdbAPIUtils()
    search_api_data = omdb_api_object.search_Movie(playwright, movie_name)
    title_api_data = omdb_api_object.getByTitle(playwright)

    # search movie name in IMDB
    imdb_search = IMDbUIValidation(browser_instance)
    imdb_search.navigateToImdb()
    imdb_search.searchMovie(movie_name)
    imdb_search.navigateToSearchedMoviePage(movie_name)
    movie_title, movie_year, movie_rating, movie_plot = imdb_search.getMovieInfoFromUI()

    assert movie_title == search_api_data["title"]
    assert movie_year == search_api_data["year"]
    assert movie_rating == title_api_data["rating"]
    assert movie_plot == title_api_data["plot"]
