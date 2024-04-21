from .soup_request import RequestSoup
import re


class Scraper():

    # constructor
    def __init__(self, url):
        self.url = url
        self.soup = RequestSoup.get(self.url)

    def get_product_info(self):
        product_info = {
            "isbn" : self.get_isbn(),
            "title" : self.get_title(),
            "author": self.get_authors(),
            "description" : self.get_desc(),
            "url": self.url,
            "cover_img": self.get_image()
            # "rating" : self.get_rating(),
            # "review count" : self.get_review_count(),
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
        
    def get_desc(self):

        try:
            desc_object = self.soup.find("div", {"id":'bookDescription_feature_div'})
            description = desc_object.text.strip()
        except AttributeError:
            description = ""

        return description
    
    def get_authors(self):

        authors = []

        try:
            auth_elements = self.soup.find("div", {"id": "bylineInfo"}).findAll("span", {"class": "author"})
            for element in auth_elements:
                author = str(element.text.strip()).split(' \n(')[0]
                authors.append(author)

        except AttributeError:
            return authors

        return authors
    
    def get_isbn(self):
        try:
            isbn_or_asin = re.search('/dp/(.*)/ref', self.url).group(1)
        except:
            return None

        return isbn_or_asin

    def get_image(self):

        try:
            image = self.soup.find("img", {"id": "landingImage"})
            image_url = image.attrs['src']
        
        except AttributeError:
            image_url = ""

        return image_url