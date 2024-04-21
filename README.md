# Web Scraper for Product Data

This web scraper is designed to retrieve product data based on a search query and upload it to a MongoDB database. It consists of several components for scraping and handling data.

## File Structure

```
web-scraper/
│
├── config/
│   └── mongo.py
│       - Instantiates a connection with the MongoDB database using PyMongo. The connection details are retrieved from environment variables    set in a .env file.
│
├── crawler.py
│   - Takes a search query and returns all product links that Amazon returns. Utilizes the `soup_request` abstract class to retrieve data from Amazon.com.
│
├── scraper.py
│   - Takes a product URL and returns a dictionary containing all product information. Also utilizes the `soup_request` abstract class to retrieve data from Amazon.com.
│
├── soup_request.py
│   - Takes a URL, sends a webpage request using the Requests library, parses the webpage using BeautifulSoup library, and returns the 'soup'.
│
├── main.py
│   - The main script responsible for running the scraper. It performs the following steps:
│       1. Passes a search query to the crawler function to obtain a list of product links.
│       2. Passes each product link to the scraper function to retrieve product data.
│       3. Collects the product data into a list.
│       4. Searches the MongoDB database for each product's ISBN.
│       5. Updates existing documents with new data if the ISBN exists in the database.
│       6. Inserts new data into the database if the ISBN does not exist.
│
└── requirements.txt
    - Contains the list of dependencies required for running the web scraper. Install them using `pip install -r requirements.txt`.

```

## Environment Variables

Environment variables are used to store sensitive information or configuration settings outside of your codebase. To set up the MongoDB connection details, follow these steps:

1. **Create a `.env` File**: In your project directory, create a file named `.env`.

2. **Define Environment Variables**: Inside the `.env` file, define the following environment variables:

    ```
    MONGO_URI=mongodb://localhost:27017/mydatabase
    DB_NAME=mydatabase
    COLLECTION_NAME=mycollection
    ```

    Replace the values with your actual MongoDB URI, database name, and collection name.

3. **Accessing Environment Variables in Python**: You can access these environment variables in your Python code using the `os` module:

    ```python
    import os

    MONGO_URI = os.getenv("MONGO_URI")
    DB_NAME = os.getenv("DB_NAME")
    COLLECTION_NAME = os.getenv("COLLECTION_NAME")
    ```

4. **Loading Environment Variables**: Before running your Python script, load the environment variables from the `.env` file. You can use the `python-dotenv` library for this purpose:

    Install `python-dotenv`:

    ```
    pip install python-dotenv
    ```

    Then, at the beginning of your Python script, add the following code to load the environment variables:

    ```python
    from dotenv import load_dotenv

    load_dotenv()
    ```

## Usage

1. Install dependencies by running `pip install -r requirements.txt`.
2. Ensure that MongoDB is running and accessible.
3. Run `main.py` to start the scraping process.

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these guidelines:
- Fork the repository.
- Create a new branch (`git checkout -b feature/your-feature`).
- Make your changes.
- Test your changes thoroughly.
- Submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.