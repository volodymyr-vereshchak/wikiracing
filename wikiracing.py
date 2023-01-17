import requests
from urllib.parse import urljoin


REQUESTS_PER_MINUTE = 100
LINKS_PER_PAGE = 200
BASE_URL = "https://uk.wikipedia.org/wiki/"


class WikiRacer:

    def find_path(self, start: str, finish: str) -> list[str]:
        start_url = urljoin(BASE_URL, start)
