import re
import logging
from core.soup_request import RequestSoup

class Scraper:
    
    def __init__(self, url: str):
        self.url = url
        self.soup = None

    async def fetch_soup(self):
        try:
            self.soup = await RequestSoup.get(self.url)
        except Exception as e:
            logging.error(f"Error fetching product page: {e}")

    async def get_product_info(self) -> dict:
        await self.fetch_soup()
        if not self.soup:
            return {}
        product_info = {
            "isbn": self.get_isbn(),
            "title": self.get_title(),
            "author": self.get_authors(),
            "description": self.get_desc(),
            "url": self.url,
            "cover_img": self.get_image()
        }
        return product_info

    def get_title(self) -> str:
        try:
            title_object = self.soup.find("span", attrs={"id": 'productTitle'})
            title = title_object.string.strip()
            return title
        except AttributeError:
            logging.error("Title not found")
            return ""

    def get_rating(self) -> str:
        return self.extract_text_with_fallback([
            ('i', {'class': 'a-icon a-icon-star a-star-4-5'}), 
            ('span', {'class': 'a-icon-alt'})
        ])

    def get_review_count(self) -> str:
        return self.extract_text_with_fallback([
            ('span', {'id': 'acrCustomerReviewText'})
        ])

    def extract_text_with_fallback(self, selectors: list) -> str:
        for tag, attrs in selectors:
            try:
                element = self.soup.find(tag, attrs=attrs)
                if element:
                    return element.string.strip()
            except AttributeError:
                continue
        return ""

    def get_desc(self) -> str:
        try:
            desc_object = self.soup.find("div", {"id": 'bookDescription_feature_div'})
            description = desc_object.text.strip()
        except AttributeError:
            logging.error("Description not found")
            description = ""
        return description

    def get_authors(self) -> list:
        authors = []
        try:
            auth_elements = self.soup.find("div", {"id": "bylineInfo"}).findAll("span", {"class": "author"})
            for element in auth_elements:
                author = str(element.text.strip()).split(' \n(')[0]
                authors.append(author)
        except AttributeError:
            logging.error("Authors not found")
        return authors

    def get_isbn(self) -> str:
        try:
            isbn_or_asin = re.search('/dp/(.*)/ref', self.url).group(1)
        except:
            logging.error("ISBN/ASIN not found")
            return None
        return isbn_or_asin

    def get_image(self) -> str:
        try:
            image = self.soup.find("img", {"id": "landingImage"})
            image_url = image.attrs['src']
        except AttributeError:
            logging.error("Image not found")
            image_url = ""
        return image_url
