from .base import Module
import requests
from bs4 import BeautifulSoup


class YouTube(Module):
    DESCRIPTION = "Searches and sends YouTube video"
    ARGC = 1

    def response(self, query, message):
        url = "https://www.youtube.com/results?search_query="
        bs = BeautifulSoup(requests.get(url + query.replace(" ", "+").lower()).text, "html.parser")
        for link in bs.find_all("a"):
            result = link.get("href")
            if result.startswith("/watch"):
                break
        return "https://www.youtube.com" + result
