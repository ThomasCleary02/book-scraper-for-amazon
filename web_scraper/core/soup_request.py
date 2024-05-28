import aiohttp
from bs4 import BeautifulSoup
from abc import ABC
import logging

class RequestSoup(ABC):
    @staticmethod
    async def get(url: str) -> BeautifulSoup:
        """
        Fetch the webpage content and parse it with BeautifulSoup asynchronously.

        :param url: The URL of the webpage to fetch.
        :return: Parsed BeautifulSoup object.
        :raises Exception: If the request fails or the status code is not 200.
        """
        HEADERS = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=HEADERS) as response:
                    response.raise_for_status()
                    content = await response.text()
            except aiohttp.ClientError as e:
                logging.error(f"Error fetching URL: {url} - {e}")
                raise Exception(f"Failed to fetch page. Status code: {response.status}")

        soup = BeautifulSoup(content, "lxml")
        return soup
