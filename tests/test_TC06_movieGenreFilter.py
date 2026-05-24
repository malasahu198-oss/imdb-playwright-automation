from pages.IMdbUIValidation import IMDbUIValidation
from pages.IMDbGenreFilter import IMDbGenreFilter


def test_filter_movies_by_genre(browser_instance):
    """TC06: Filter movies by genre"""
    # Setup
    ui_validation = IMDbUIValidation(browser_instance)
    genre_filter = IMDbGenreFilter(browser_instance)
    genre_name = "Action"

    # Navigate and filter
    ui_validation.navigateToImdb()
    genre_filter.navigate_to_advanced_search()
    genre_filter.select_genre(genre_name)
    genre_filter.apply_filters()

    # Assertions (IN TEST)
    assert genre_filter.is_results_loaded(), "Results should load after filter"
    assert genre_filter.get_filtered_results_count() > 0, "Should have filtered results"
