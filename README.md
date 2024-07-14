# Amazon Product Data Scraper API

This project is an API that provides access to a web scraper designed to search for products on Amazon and extract detailed information about them.

## Features

- Search for products on Amazon by keyword
- Extract product details such as title, author, description, ISBN, and cover image
- Asynchronous requests for improved performance
- RESTful API built with FastAPI

## Prerequisites

- Python 3.7+

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/amazon-scraper-api.git
    cd amazon-scraper-api
    ```

2. Create a virtual environment and activate it:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:

    ```sh
    pip install -r requirements.txt
    ```

## Usage

Run the FastAPI server:

```sh
uvicorn main:app --reload
```

The API will be available at http://localhost:8000.

## API Endpoints

- POST /search: Search for products and retrieve their details

 - Request body:
 ```json
 {
   "keywords": "string",
   "num_results": "integer"
 }
```
 - Response: Array of product information objects

## API Documentation
Once the server is running, you can access the interactive API documentation:

Swagger UI: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc

## Project Structure

- **main.py**: The entry point of the application. Contains the FastAPI app and endpoint definitions.
- **core/crawler**.py: Contains the Crawler class that fetches product links from Amazon search results.
- **core/scraper**.py: Contains the Scraper class that extracts detailed product information from individual product pages.
- **core/soup_request**.py: Contains the RequestSoup class that handles HTTP requests and parses responses with BeautifulSoup.
- **utils/helpers.py**: Contains utility functions, including logging setup and URL creation.

## Dependencies

- fastapi
- uvicorn
- aiohttp
- beautifulsoup4
- pydantic

## Contributing

Feel free to fork the repository and submit pull requests. Any enhancements, bug fixes, or suggestions are welcome.

## License
This project is licensed under the MIT License. See the [LICENSE](https://github.com/git/git-scm.com/blob/main/MIT-LICENSE.txt) file for more details.