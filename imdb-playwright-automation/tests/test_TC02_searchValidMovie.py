from pages.IMdbUIValidation import IMDbUIValidation


def test_searchValidMovie(browser_instance):
    imdb_search = IMDbUIValidation(browser_instance)
    imdb_search.searchMovie("Inception")
