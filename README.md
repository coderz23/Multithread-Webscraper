## README: Web Scraper

This Python script scrapes data from a website and parses it based on different configurations for specific sites.

### Features

* Scrapes multiple pages concurrently for faster execution.
* Handles errors during page fetching and parsing gracefully.
* Supports different site configurations with custom selectors for titles, authors, tags, prices, and ratings.
* Prints the scraped data in a user-friendly format.

### Requirements

* Python 3
* Libraries:
    * `requests` - for making HTTP requests
    * `beautifulsoup4` - for parsing HTML content
    * `concurrent.futures` - for concurrent scraping

### Usage

1. Install the required libraries:

   ```bash
   pip install requests beautifulsoup4 concurrent.futures
   ```

2. Edit the script:

   * Change the `site` variable in the `main` function to "quotes" or "books" depending on which website you want to scrape.
   * You can modify the configuration dictionaries (`SITE_CONFIGS`) for these sites to adjust the selectors used for scraping specific data points.

3. Run the script:

   ```bash
   python scraper.py
   ```

### Output

The script will print the scraped data including titles, authors (for quotes), tags (for quotes), prices (for books), and ratings (for books) in a well-formatted way. It will also display the total time taken to complete the scraping process.
"# Multithread-Webscraper" 
