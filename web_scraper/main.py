from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import asyncio
from core.crawler import Crawler
from core.scraper import Scraper
from utils.helpers import setup_logging

app = FastAPI()

setup_logging()

class SearchRequest(BaseModel):
    keywords: str
    num_results: int

class ProductInfo(BaseModel):
    isbn: str
    title: str
    author: List[str]
    description: str
    url: str
    cover_img: str

@app.post("/search", response_model=List[ProductInfo])
async def search_products(request: SearchRequest):
    if request.num_results <= 0:
        raise HTTPException(status_code=400, detail="Number of results must be greater than 0")
    
    # Get product links
    product_links = await Crawler.extract_product_links(request.keywords)
    
    # Limit the number of links to scrape
    product_links = product_links[:request.num_results]
    
    # Scrape product information
    tasks = [Scraper(url).get_product_info() for url in product_links]
    results = await asyncio.gather(*tasks)
    
    # Filter out any empty results
    valid_results = [ProductInfo(**result) for result in results if result]
    
    return valid_results

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)