import logging
from utils.helpers import create_search_url
from core.soup_request import RequestSoup

class Crawler:
    @staticmethod
    async def extract_product_links(search_query: str) -> list:
        base_url = "https://www.amazon.com/s"
        try:
            soup = await RequestSoup.get(create_search_url(base_url, search_query))
        except Exception as e:
            logging.error(f"Error fetching search page: {e}")
            return []

        link_tags = soup.find_all("a", attrs={'class': 'a-link-normal s-no-outline'})
        urls_list = ["https://www.amazon.com" + tag.get('href') for tag in link_tags]

        return urls_list
