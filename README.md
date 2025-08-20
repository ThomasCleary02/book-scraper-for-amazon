# Amazon Product Data Scraper API

⚠️ **IMPORTANT LEGAL DISCLAIMER** ⚠️

This project is provided for **EDUCATIONAL AND RESEARCH PURPOSES ONLY**. 

**Web scraping may violate websites' Terms of Service and could result in legal consequences.** 

- This API is **NOT intended for commercial use**
- **Use at your own risk** - we are not responsible for any legal issues
- Consider using **official APIs** (like Amazon Product Advertising API) for production applications
- **Respect robots.txt** and website terms of service
- **Implement proper rate limiting** to avoid overwhelming servers

## 🚨 Legal and Ethical Considerations

- **Terms of Service**: Web scraping may violate Amazon's Terms of Service
- **Rate Limiting**: Always implement reasonable delays between requests
- **User Agents**: Rotate user agents to avoid detection
- **Proxies**: Consider using proxy rotation for high-volume requests
- **Compliance**: Ensure compliance with local laws and regulations
- **Alternative**: Use Amazon's official Product Advertising API for commercial applications

## 🚀 Production Features

- **Rate Limiting**: Configurable rate limiting (default: 10 requests/minute)
- **API Key Authentication**: Secure access control
- **Redis Caching**: Response caching to reduce server load
- **Error Handling**: Comprehensive error handling and logging
- **Health Checks**: Monitoring endpoints for production deployment
- **CORS Support**: Configurable cross-origin resource sharing
- **Input Validation**: Pydantic models for request validation
- **Timeout Protection**: Request timeouts to prevent hanging
- **Logging**: Structured logging for production monitoring

## 📋 Prerequisites

- Python 3.8+
- Redis server (for caching)
- Valid API key (for authentication)

## 🔧 Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/amazon-scraper-api.git
    cd amazon-scraper-api
    ```

2. Create a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up environment variables:
    ```sh
    cp .env.example .env
    # Edit .env with your configuration
    ```

## ⚙️ Configuration

Create a `.env` file with the following variables:

```env
# API Configuration
ENVIRONMENT=development
DEBUG=false
PORT=8000
LOG_LEVEL=info

# Security
API_KEYS=your-api-key-1,your-api-key-2
SECRET_KEY=your-secret-key-change-in-production

# Rate Limiting
RATE_LIMIT_PER_MINUTE=10

# Redis
REDIS_URL=redis://localhost:6379
REDIS_TTL=3600

# CORS
ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com
```

## 🚀 Usage

### Development
```sh
uvicorn web_scraper.main:app --reload
```

### Production
```sh
uvicorn web_scraper.main:app --host 0.0.0.0 --port 8000
```

## 🔐 Authentication

All API endpoints require authentication via API key in the Authorization header:

```bash
curl -X POST "http://localhost:8000/search" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"keywords": "python programming", "num_results": 5}'
```

## 🔗 API Endpoints

### Health Check
- `GET /health` - Service health status

### Search Products
- `POST /search` - Search for products by keywords
  - Rate limited to 10 requests per minute
  - Requires valid API key
  - Returns cached results when available

## 📁 Project Structure

```
web_scraper/
├── main.py # FastAPI application entry point
├── config.py # Configuration settings
├── core/
│ ├── crawler.py # Web crawling logic
│ ├── scraper.py # Data extraction
│ └── soup_request.py # HTTP request handling
└── utils/
└── helpers.py # Utility functions
```


## �� Deployment Options

### Cloud Platforms

#### Railway (Recommended for beginners)
```bash
npm install -g @railway/cli
railway login
railway init
railway up
```

#### Render
1. Connect GitHub repo to Render
2. Create new Web Service
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn web_scraper.main:app --host 0.0.0.0 --port $PORT`
5. Add Redis add-on

#### DigitalOcean App Platform
1. Connect GitHub repo
2. Choose Python app
3. Add Redis database
4. Set environment variables

### Container Deployment
- **Docker + AWS ECS**: Production-grade scalability
- **Google Cloud Run**: Serverless containers
- **Azure Container Instances**: Microsoft's container service

### Serverless
- **AWS Lambda + API Gateway**: Pay-per-use model
- **Vercel**: Simple Python API deployment
- **Netlify Functions**: Easy serverless functions

## 📊 Monitoring

- **Health Checks**: `/health` endpoint for uptime monitoring
- **Rate Limiting**: Built-in rate limiting with configurable limits
- **Logging**: Structured logging for production debugging
- **Caching**: Redis-based response caching

## 🔧 Troubleshooting

### Common Issues

1. **Redis Connection Failed**
   - Ensure Redis server is running
   - Check REDIS_URL environment variable
   - API will work without Redis (no caching)

2. **Rate Limiting**
   - Default: 10 requests per minute per IP
   - Adjust RATE_LIMIT_PER_MINUTE in environment

3. **Authentication Errors**
   - Verify API_KEYS environment variable
   - Check Authorization header format

4. **Scraping Failures**
   - Amazon may block requests
   - Check logs for specific error messages
   - Consider using proxies for production

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚖️ Disclaimer

This software is provided "as is" without warranty of any kind. The authors are not responsible for any damages or legal issues that may arise from its use. Users are responsible for ensuring compliance with applicable laws and website terms of service.

## 🔗 Alternatives

For production use, consider these official alternatives:
- [Amazon Product Advertising API](https://webservices.amazon.com/paapi5/documentation/)
- [Google Shopping API](https://developers.google.com/shopping-content)
- [eBay Finding API](https://developer.ebay.com/DevZone/finding/Concepts/FindingAPIGuide.html)

---

**Remember**: Web scraping should be done responsibly and ethically. Always respect website terms of service and implement proper rate limiting.