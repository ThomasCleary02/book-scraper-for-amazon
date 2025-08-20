import os
import time
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
import asyncio
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
# Fix the import paths - add web_scraper prefix
from web_scraper.core.crawler import Crawler
from web_scraper.core.scraper import Scraper
from web_scraper.utils.helpers import setup_logging, get_redis_client, verify_api_key
import logging
import json

# Setup logging
setup_logging()

# Initialize FastAPI app
app = FastAPI(
    title="Amazon Product Data Scraper API",
    description="An API for scraping product data from Amazon based on search keywords",
    version="1.0.0",
    docs_url="/docs" if os.getenv("ENVIRONMENT") != "production" else None,
    redoc_url="/redoc" if os.getenv("ENVIRONMENT") != "production" else None
)

# Rate limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Models
class SearchRequest(BaseModel):
    keywords: str = Field(..., min_length=1, max_length=200, description="Search keywords for product search")
    num_results: int = Field(..., ge=1, le=50, description="Number of results to return (max 50)")

class ProductInfo(BaseModel):
    isbn: Optional[str] = None
    title: Optional[str] = None
    author: Optional[List[str]] = None
    description: Optional[str] = None
    url: Optional[str] = None
    cover_img: Optional[str] = None
    price: Optional[str] = None
    rating: Optional[float] = None
    review_count: Optional[int] = None

class HealthResponse(BaseModel):
    status: str
    timestamp: float
    version: str

# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint for monitoring"""
    return HealthResponse(
        status="healthy",
        timestamp=time.time(),
        version="1.0.0"
    )

# Rate limited and authenticated search endpoint
@app.post("/search", response_model=List[ProductInfo])
@limiter.limit("10/minute")  # Rate limit: 10 requests per minute
async def search_products(
    request: Request,
    search_request: SearchRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Search for products and retrieve their details.
    
    Rate limited to 10 requests per minute per IP address.
    Requires valid API key in Authorization header.
    """
    # Verify API key
    if not verify_api_key(credentials.credentials):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    
    try:
        # Check cache first
        redis_client = get_redis_client()
        cache_key = f"search:{search_request.keywords}:{search_request.num_results}"
        
        if redis_client:
            try:
                cached_result = redis_client.get(cache_key)
                if cached_result:
                    # Parse cached JSON back to ProductInfo objects
                    cached_data = json.loads(cached_result)
                    return [ProductInfo(**item) for item in cached_data]
            except Exception as e:
                logging.warning(f"Redis cache error: {e}")
        
        # Get product links
        product_links = await Crawler.extract_product_links(search_request.keywords)
        
        if not product_links:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No products found for the given keywords"
            )
        
        # Limit the number of links to scrape
        product_links = product_links[:search_request.num_results]
        
        # Scrape product information with timeout
        tasks = [Scraper(url).get_product_info() for url in product_links]
        results = await asyncio.wait_for(
            asyncio.gather(*tasks, return_exceptions=True),
            timeout=30.0  # 30 second timeout
        )
        
        # Filter out any empty results and exceptions
        valid_results = []
        for result in results:
            if isinstance(result, Exception):
                continue
            if result:
                try:
                    valid_results.append(ProductInfo(**result))
                except Exception:
                    continue
        
        if not valid_results:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to extract product information"
            )
        
        # Cache results for 1 hour (only if Redis is available)
        if redis_client and valid_results:
            try:
                # Convert Pydantic models to dict for JSON serialization
                cache_data = [result.dict() for result in valid_results]
                redis_client.setex(cache_key, 3600, json.dumps(cache_data))
            except Exception as e:
                logging.warning(f"Failed to cache results: {e}")
        
        return valid_results
        
    except asyncio.TimeoutError:
        raise HTTPException(
            status_code=status.HTTP_408_REQUEST_TIMEOUT,
            detail="Request timed out. Please try again."
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Amazon Product Data Scraper API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs" if os.getenv("ENVIRONMENT") != "production" else "Documentation disabled in production"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=int(os.getenv("PORT", 8000)),
        log_level=os.getenv("LOG_LEVEL", "info")
    )