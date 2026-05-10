from conftest import browser_instance
from pages.IMdbUIValidation import IMDbUIValidation


def test_searchInvalidMovie(browser_instance):
    imdb_search = IMDbUIValidation(browser_instance)
    imdb_search.searchMovie("xyzabc123")


def test_IMdbLogoClick(browser_instance):
    imdb_search = IMDbUIValidation(browser_instance)
    imdb_search.navigateToHomePage()
