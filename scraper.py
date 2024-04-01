from soup_request import RequestSoup

class Scraper:

    # constructor creates a soup object by called the RequestSoup
    def __init__(self, product_url):
        self.url = product_url
        self.soup = RequestSoup.get(product_url)

    # method to extract all product data
    # and return a dictionary of data points
    def scrape(self):

        product_info ={
            "title" : self.get_title(),
            "rating" : self.get_rating(),
            "review count" : self.get_review_count()
        }

        return product_info

    # method to extract title from product page
    def get_title(self):

        title_object = self.soup.find("span", attrs={"id":'productTitle'})
        title = title_object.string.strip()

        return title
    
    # method to extract product rating
    def get_rating(self):

        try:
            rating = self.soup.find("i", attrs={'class':'a-icon a-icon-star a-star-4-5'}).string.strip()
            
        except AttributeError:
            
            try:
                rating = self.soup.find("span", attrs={'class':'a-icon-alt'}).string.strip()
            except:
                rating = ""	

        return rating
    
    # method to extract number of reviews
    def get_review_count(self):
        try:
            review_count = self.soup.find("span", attrs={'id':'acrCustomerReviewText'}).string.strip()
            
        except AttributeError:
            review_count = ""	

        return review_count
    
