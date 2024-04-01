from soup_request import RequestSoup

class Crawler:

    # constructor defines a value for search_query
    def __init__(self, search_query):
        self.search_query = search_query

    # create the search url using the search query
    def create_url(self):
        url = "https://www.amazon.com/s?k=" + self.search_query.replace(" ", "+")
        return url

    # method to extract urls from search page
    def crawl(self):

        self.soup = RequestSoup.get(self.create_url())

        link_tags = self.soup.find_all("a", attrs={'class':'a-link-normal s-no-outline'})

        urls_list = []

        for tag in link_tags:
            url = "https://www.amazon.com" + tag.get('href')
            urls_list.append(url)

        return urls_list
        