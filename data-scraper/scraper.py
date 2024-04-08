from soup_request import RequestSoup


# method to extract title from product page
def get_title(soup):

    title_object = soup.find("span", attrs={"id":'productTitle'})
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
    
# method to return a dictionary of data 
def scrape(url):

    soup = RequestSoup.get(url)

    product_info = {
        "title" : get_title(soup),
        "rating" : get_rating(),
        "review count" : get_review_count()
    }

    return product_info