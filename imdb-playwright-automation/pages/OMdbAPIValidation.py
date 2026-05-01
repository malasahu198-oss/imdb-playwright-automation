import playwright
from playwright.sync_api import Playwright
from dotenv import load_dotenv
import os

load_dotenv()
apiKey = os.getenv("OMDB_API_KEY")


class OMdbAPIUtils:

    def __init__(self):
        self.response_imdb_id = None
        self.response_title = None

    def search_Movie(self, playwright: Playwright):
        api_req_context = playwright.request.new_context()

        response = api_req_context.get(url="https://www.omdbapi.com/",
                                       params={"apiKey": apiKey, "s": "The Crack: Inception"})

        assert response.status == 200, f"expected 200, got {response.status}"
        response_body = response.json()
        self.response_title = response_body["Search"][0]["Title"]
        response_year = response_body["Search"][0]["Year"]
        self.response_imdb_id = response_body["Search"][0]["imdbID"]
        return {"title": self.response_title, "year": response_year, "imdb_id": self.response_imdb_id}

    def getByTitle(self, playwright: Playwright):
        api_req_context = playwright.request.new_context()
        titleResponse = api_req_context.get(url="https://www.omdbapi.com/?",
                                            params={"apiKey": apiKey, "t": self.response_title, "type": "movie"})

        assert titleResponse.status == 200, f"expected 200, got {titleResponse.status}"
        response_body = titleResponse.json()
        response_plot = response_body["Plot"]
        response_rating = response_body["imdbRating"]
        response_id = response_body["imdbID"]

        assert self.response_imdb_id == response_id
        return {"plot": response_plot, "rating": response_rating}
