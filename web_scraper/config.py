import os
from typing import List

class Settings:
    # API Configuration
    API_TITLE: str = "Amazon Product Data Scraper API"
    API_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Security
    API_KEYS: List[str] = os.getenv("API_KEYS", "").split(",") if os.getenv("API_KEYS") else []
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "10"))
    
    # Redis Configuration
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    REDIS_TTL: int = int(os.getenv("REDIS_TTL", "3600"))  # 1 hour
    
    # CORS
    ALLOWED_ORIGINS: List[str] = os.getenv("ALLOWED_ORIGINS", "*").split(",")
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "info")

settings = Settings()
