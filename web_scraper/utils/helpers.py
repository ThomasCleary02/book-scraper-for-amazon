import logging
from urllib.parse import urlencode

def create_search_url(base_url: str, query: str) -> str:
    """
    Create a search URL using the base URL and search query.

    :param base_url: The base URL of the search site (e.g., Amazon).
    :param query: The search query string.
    :return: Formatted search URL.
    """
    params = {'k': query.replace(" ", "+")}
    return f"{base_url}?{urlencode(params)}"

def setup_logging(log_level=logging.INFO):
    """
    Setup logging configuration.

    :param log_level: Logging level, default is logging.INFO.
    """
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )
