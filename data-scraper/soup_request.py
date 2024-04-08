import requests
from bs4 import BeautifulSoup
from abc import ABC

class RequestSoup(ABC):

    # function that combines the functionality
    # of requests and BeautifulSoup into one
    def get(url):
       
        HEADERS = ({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'
        })

        webpage = requests.get(url, headers=HEADERS)
        assert webpage.status_code == 200
        soup = BeautifulSoup(webpage.content, "lxml")

        return soup