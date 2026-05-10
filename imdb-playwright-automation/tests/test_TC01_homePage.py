from pages.IMdbUIValidation import IMDbUIValidation


def test_homePageLoadedImdb(browser_instance):
    imdb_search = IMDbUIValidation(browser_instance)
    imdb_search.navigateToImdb()
