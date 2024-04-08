from scraper import Scraper
from crawler import Crawler


if __name__=="__main__":

    search_query = "edward steers jr"

    products = []

    new_search = Crawler(search_query)
    target_urls = new_search.crawl()

    for url in target_urls:
        product = Scraper(url)
        products.append(product.scrape())

    for product in products:
        for key, value in product.items():
            print(key, " : ", value)
        print("\n")