# Web Scraper for Amazon Books

This project is a web scraper designed to search for books on Amazon, extract detailed information about them, and store the information in a MongoDB database.

## Features

- Search for books on Amazon by keyword
- Extract book details such as title, author, description, ISBN, and cover image
- Store book information in a MongoDB database
- Asynchronous requests for improved performance

## Prerequisites

- Python 3.7+
- MongoDB instance (local or remote)

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/web_scraper.git
    cd web_scraper
    ```

2. Create a virtual environment and activate it:

    ```sh
    python -m venv venv
    source venv/bin/activate
    ```

3. Install the required dependencies:

    ```sh
    pip install -r requirements.txt
    ```

4. Set up the environment variables:

    Create a `.env` file in the root directory of the project and add the following variables:

    ```env
    MONGO_URI=mongodb://localhost:27017/mydatabase
    DB_NAME=mydatabase
    COLLECTION_NAME=mycollection
    ```

    Adjust the values according to your MongoDB setup.

## Usage

Run the main script to start scraping:

```sh
python main.py
```

The script will search for books with the query "edward steers jr", extract information, and store it in the specified MongoDB collection.

## Project Structure

- **main.py**: The entry point of the application. Handles the overall flow of scraping and storing book information.
- **core/crawler.py**: Contains the Crawler class that fetches product links from Amazon search results.
- **core/scraper.py**: Contains the Scraper class that extracts detailed book information from individual product pages.
- **core/soup_request.py**: Contains the RequestSoup class that handles HTTP requests and parses responses with BeautifulSoup.
- **config/mongo.py**: Contains the MongoDB class that manages the connection and operations with the MongoDB database.
- **utils/helpers.py**: Contains utility functions, including logging setup and URL creation.

## Dependencies

- aiohttp
- beautifulsoup4
- python-dotenv
- pymongo
- requests

## Contributing

Feel free to fork the repository and submit pull requests. Any enhancements, bug fixes, or suggestions are welcome.

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/git/git-scm.com/blob/main/MIT-LICENSE.txt) file for more details.