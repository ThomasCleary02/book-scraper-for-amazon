# Amazon Book Scraper API Documentation

## Overview

The Amazon Book Scraper API is a production-ready REST API that allows you to search for books on Amazon and extract detailed product information. Built with FastAPI, it provides authentication, rate limiting, and comprehensive book data extraction.

**Base URL**: `https://bookscraperapi-production.up.railway.app`

## Features

- 🔍 **Book Search**: Search Amazon by keywords
- 📊 **Rich Data**: Extract title, author, price, rating, reviews, cover image, and description
- 🔐 **Authentication**: API key-based access control
- ⚡ **Rate Limiting**: 10 requests per minute per IP
- 🚀 **Production Ready**: Deployed on Railway with monitoring
- 📝 **Comprehensive Logging**: Full request/response logging

## Authentication

All API endpoints require authentication via API key in the Authorization header.

```http
Authorization: Bearer YOUR_API_KEY
```

### Getting an API Key

Contact the API administrator to obtain your API key. The key should be included in all requests.

## Rate Limiting

- **Limit**: 10 requests per minute per IP address
- **Headers**: Rate limit information is included in response headers
- **Exceeded**: Returns `429 Too Many Requests` when limit is exceeded

## Endpoints

### 1. Health Check

Check the API service status and health.

```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": 1703123456.789,
  "version": "1.0.0"
}
```

**Status Codes:**
- `200 OK`: Service is healthy
- `500 Internal Server Error`: Service issues

### 2. Root Information

Get basic API information.

```http
GET /
```

**Response:**
```json
{
  "message": "Amazon Product Data Scraper API",
  "version": "1.0.0",
  "status": "running",
  "docs": "Documentation disabled in production"
}
```

**Status Codes:**
- `200 OK`: API information returned

### 3. Search Books

Search for books on Amazon by keywords and retrieve detailed information.

```http
POST /search
```

**Headers:**
```http
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
```

**Request Body:**
```json
{
  "keywords": "python programming",
  "num_results": 3
}
```

**Parameters:**
- `keywords` (string, required): Search terms for book search
  - Min length: 1
  - Max length: 200
- `num_results` (integer, required): Number of results to return
  - Min value: 1
  - Max value: 50

**Response:**
```json
[
  {
    "isbn": "B0CSY7BL6Q",
    "title": "Python Programming for Beginners: The Complete Python Coding Crash Course",
    "author": ["codeprowess"],
    "description": "UPDATED VERSION AUGUST 2025...",
    "url": "https://www.amazon.com/...",
    "cover_img": "https://m.media-amazon.com/images/I/517KYcz2AJL._SX342_SY445_.jpg",
    "price": "$59.95",
    "rating": 4.5,
    "review_count": 723
  }
]
```

**Response Fields:**
- `isbn`: Amazon ASIN (Amazon Standard Identification Number)
- `title`: Book title
- `author`: Array of author names
- `description`: Book description/summary
- `url`: Amazon product page URL
- `cover_img`: Book cover image URL
- `price`: Book price (may be missing)
- `rating`: Book rating out of 5 (may be missing)
- `review_count`: Number of customer reviews (may be missing)

**Status Codes:**
- `200 OK`: Search completed successfully
- `400 Bad Request`: Invalid request parameters
- `401 Unauthorized`: Invalid or missing API key
- `404 Not Found`: No books found for the given keywords
- `408 Request Timeout`: Request timed out (30 second limit)
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error during scraping

## Error Responses

### Standard Error Format
```json
{
  "detail": "Error message description"
}
```

### Common Error Codes

#### 400 Bad Request
```json
{
  "detail": "Number of results must be greater than 0"
}
```

#### 401 Unauthorized
```json
{
  "detail": "Invalid API key"
}
```

#### 404 Not Found
```json
{
  "detail": "No products found for the given keywords"
}
```

#### 408 Request Timeout
```json
{
  "detail": "Request timed out. Please try again."
}
```

#### 429 Too Many Requests
```json
{
  "detail": "Rate limit exceeded"
}
```

#### 500 Internal Server Error
```json
{
  "detail": "Internal server error: [error details]"
}
```

## Usage Examples

### cURL Examples

#### Health Check
```bash
curl https://bookscraperapi-production.up.railway.app/health
```

#### Search for Python Books
```bash
curl -X POST "https://bookscraperapi-production.up.railway.app/search" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"keywords": "python programming", "num_results": 5}'
```

#### Search for Machine Learning Books
```bash
curl -X POST "https://bookscraperapi-production.up.railway.app/search" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"keywords": "machine learning", "num_results": 3}'
```

### Python Examples

#### Using requests library
```python
import requests
import json

# API configuration
API_BASE_URL = "https://bookscraperapi-production.up.railway.app"
API_KEY = "YOUR_API_KEY"

# Headers
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Search for books
def search_books(keywords, num_results=5):
    url = f"{API_BASE_URL}/search"
    data = {
        "keywords": keywords,
        "num_results": num_results
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

# Example usage
books = search_books("python programming", 3)
if books:
    for book in books:
        print(f"Title: {book['title']}")
        print(f"Author: {', '.join(book['author'])}")
        print(f"Price: {book.get('price', 'N/A')}")
        print(f"Rating: {book.get('rating', 'N/A')}")
        print("---")
```

#### Using httpx (async)
```python
import httpx
import asyncio

async def search_books_async(keywords, num_results=5):
    API_BASE_URL = "https://bookscraperapi-production.up.railway.app"
    API_KEY = "YOUR_API_KEY"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "keywords": keywords,
        "num_results": num_results
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{API_BASE_URL}/search",
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

# Example usage
async def main():
    books = await search_books_async("python programming", 3)
    if books:
        for book in books:
            print(f"Title: {book['title']}")

asyncio.run(main())
```

### JavaScript/Node.js Examples

#### Using fetch
```javascript
const API_BASE_URL = 'https://bookscraperapi-production.up.railway.app';
const API_KEY = 'YOUR_API_KEY';

async function searchBooks(keywords, numResults = 5) {
    try {
        const response = await fetch(`${API_BASE_URL}/search`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${API_KEY}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                keywords: keywords,
                num_results: numResults
            })
        });

        if (response.ok) {
            const books = await response.json();
            return books;
        } else {
            console.error(`Error: ${response.status} - ${response.statusText}`);
            return null;
        }
    } catch (error) {
        console.error('Request failed:', error);
        return null;
    }
}

// Example usage
searchBooks('python programming', 3)
    .then(books => {
        if (books) {
            books.forEach(book => {
                console.log(`Title: ${book.title}`);
                console.log(`Author: ${book.author.join(', ')}`);
                console.log(`Price: ${book.price || 'N/A'}`);
                console.log(`Rating: ${book.rating || 'N/A'}`);
                console.log('---');
            });
        }
    });
```

## Best Practices

### 1. Error Handling
Always check response status codes and handle errors gracefully:
```python
if response.status_code == 200:
    books = response.json()
elif response.status_code == 429:
    print("Rate limit exceeded, wait before retrying")
elif response.status_code == 401:
    print("Invalid API key")
else:
    print(f"Error: {response.status_code}")
```

### 2. Rate Limiting
- Respect the 10 requests per minute limit
- Implement exponential backoff for retries
- Cache results when possible

### 3. Request Optimization
- Use appropriate `num_results` values
- Avoid very broad keywords that might return too many results
- Consider caching frequently requested searches

### 4. Data Validation
- Always validate response data before use
- Handle missing fields gracefully (price, rating, etc.)
- Sanitize user input before sending requests

## Monitoring and Health

### Health Check Endpoint
Use the `/health` endpoint to monitor API status:
- Check service uptime
- Verify API version
- Monitor response times

### Rate Limit Monitoring
Monitor rate limit headers in responses:
- `X-RateLimit-Limit`: Maximum requests per minute
- `X-RateLimit-Remaining`: Remaining requests in current window
- `X-RateLimit-Reset`: Time when rate limit resets

## Troubleshooting

### Common Issues

#### 1. Authentication Errors
- Verify API key is correct
- Check Authorization header format
- Ensure API key is active

#### 2. Rate Limiting
- Reduce request frequency
- Implement request queuing
- Use caching for repeated searches

#### 3. Timeout Errors
- Reduce `num_results` for faster responses
- Check network connectivity
- Verify Amazon is accessible

#### 4. No Results Found
- Try different keywords
- Check spelling
- Use more specific search terms

### Getting Help

If you encounter issues:
1. Check the error response details
2. Verify your request format
3. Check API status at `/health`
4. Contact API administrator

## Changelog

### Version 1.0.0
- Initial API release
- Book search functionality
- Authentication and rate limiting
- Comprehensive book data extraction

## Support

For technical support or questions:
- Check this documentation
- Review error responses
- Contact the API administrator

---

**Note**: This API is for educational and research purposes. Please respect Amazon's Terms of Service and implement appropriate rate limiting in your applications.
