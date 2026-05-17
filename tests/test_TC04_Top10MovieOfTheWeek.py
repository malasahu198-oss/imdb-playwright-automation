from pages.IMdbUIValidation import IMDbUIValidation


def test_validateTop10MoviedOfTheWeek(browser_instance):
    imdb_search = IMDbUIValidation(browser_instance)
    imdb_search.top10moviesOfTheWeek()
