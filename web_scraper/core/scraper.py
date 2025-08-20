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
            "cover_img": self.get_image(),
            "price": self.get_price(),
            "rating": self.get_rating(),
            "review_count": self.get_review_count()
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

    def get_rating(self) -> float:
        try:
            # Extract rating from star display
            rating_element = self.soup.find('i', {'class': 'a-icon-star'})
            if rating_element:
                rating_text = rating_element.get('class', [])
                for class_name in rating_text:
                    if 'a-star-' in class_name:
                        # Extract rating like "4-5" and convert to float
                        rating_match = re.search(r'a-star-(\d+)-(\d+)', class_name)
                        if rating_match:
                            whole = int(rating_match.group(1))
                            fraction = int(rating_match.group(2))
                            return whole + (fraction / 10.0)
            
            return None
        except Exception as e:
            logging.error(f"Error extracting rating: {e}")
            return None

    def get_review_count(self) -> int:
        try:
            # Extract review count
            review_element = self.soup.find('span', {'id': 'acrCustomerReviewText'})
            if review_element:
                review_text = review_element.get_text()
                # Extract number from text like "1,234 customer reviews"
                review_match = re.search(r'(\d+(?:,\d+)*)', review_text)
                if review_match:
                    return int(review_match.group(1).replace(',', ''))
            return None
        except Exception as e:
            logging.error(f"Error extracting review count: {e}")
            return None

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

    def get_price(self) -> str:
        try:
            # Try multiple price selectors for different page layouts
            price_selectors = [
                ('span', {'class': 'a-price-whole'}),
                ('span', {'class': 'a-offscreen'}),
                ('span', {'class': 'a-price a-text-price'})
            ]
            
            for tag, attrs in price_selectors:
                element = self.soup.find(tag, attrs=attrs)
                if element:
                    price_text = element.get_text().strip()
                    if price_text and '$' in price_text:
                        return price_text
            
            return ""
        except Exception as e:
            logging.error(f"Error extracting price: {e}")
            return ""
