from pages.IMdbUIValidation import IMDbUIValidation


def test_searchValidMovie(browser_instance, movie_mame):
    imdb_search = IMDbUIValidation(browser_instance)
    imdb_search.searchMovie(movie_mame)
