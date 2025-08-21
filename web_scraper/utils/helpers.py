import logging
import os
import redis
from urllib.parse import quote_plus
from typing import Optional

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=getattr(logging, os.getenv("LOG_LEVEL", "INFO").upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('app.log') if os.getenv("ENVIRONMENT") == "production" else logging.NullHandler()
        ]
    )

def create_search_url(base_url: str, search_query: str) -> str:
    """Create Amazon search URL with proper encoding"""
    encoded_query = quote_plus(search_query)
    return f"{base_url}?k={encoded_query}"

def get_redis_client() -> redis.Redis:
    """Get Redis client instance"""
    try:
        return redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))
    except Exception as e:
        logging.warning(f"Redis connection failed: {e}")
        return None

def verify_api_key(api_key: str) -> bool:
    """Verify if the provided API key is valid"""
    valid_keys = os.getenv("API_KEYS", "").split(",")
    return api_key in valid_keys and api_key.strip() != ""

def sanitize_input(text: str) -> str:
    """Sanitize user input to prevent injection attacks"""
    if not text:
        return ""
    # Remove potentially dangerous characters
    dangerous_chars = ['<', '>', '"', "'", '&', ';', '(', ')', '{', '}']
    for char in dangerous_chars:
        text = text.replace(char, '')
    return text.strip()
