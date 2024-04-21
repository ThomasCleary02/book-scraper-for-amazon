from .soup_request import RequestSoup

# create the search url using the search query
def create_url(string: str):
    url = "https://www.amazon.com/s?k=" + string.replace(" ", "+")
    return url

# method to extract urls from search page
def crawl(search_query: str):

    soup = RequestSoup.get(create_url(search_query))
 
    link_tags = soup.find_all("a", attrs={'class':'a-link-normal s-no-outline'})

    urls_list = []

    for tag in link_tags:
        url = "https://www.amazon.com" + tag.get('href')
        urls_list.append(url)

    return urls_list
        