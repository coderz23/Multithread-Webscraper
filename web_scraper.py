import requests
from bs4 import BeautifulSoup
import concurrent.futures
import time

# Define the number of pages to scrape
NUM_PAGES = 5

# Define configurations for different sites
SITE_CONFIGS = {
    'quotes': {
        'base_url': 'http://quotes.toscrape.com/page/{}',
        'article_selector': 'div.quote',
        'title_selector': 'span.text',
        'author_selector': 'small.author',
        'tags_selector': 'a.tag'
    },
    'books': {
        'base_url': 'https://books.toscrape.com/catalogue/page-{}.html',
        'article_selector': 'article.product_pod',
        'title_selector': 'h3 a',
        'price_selector': 'p.price_color',
        'rating_selector': 'p.star-rating'
    }
}

def fetch_page(url):
    """
    Fetches the HTML content of the page.
    
    Args:
        url (str): The URL of the page to fetch.
    
    Returns:
        str: The HTML content of the page, or None if an error occurred.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def parse_page(html_content, config):
    """
    Parses the HTML content based on the provided configuration.
    
    Args:
        html_content (str): The HTML content of the page.
        config (dict): The configuration dictionary for the site.
    
    Returns:
        list: A list of tuples containing parsed item data.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    items = []

    for item_div in soup.select(config['article_selector']):
        try:
            title = item_div.select_one(config['title_selector']).get_text(strip=True)
            if 'author_selector' in config:
                # Parsing configuration for quotes
                author = item_div.select_one(config['author_selector']).get_text(strip=True)
                tags = [tag.get_text(strip=True) for tag in item_div.select(config['tags_selector'])]
                items.append((title, author, tags))
            else:
                # Parsing configuration for books
                price = item_div.select_one(config['price_selector']).get_text(strip=True)
                rating = item_div.select_one(config['rating_selector'])['class'][1]
                items.append((title, price, rating))
        except (AttributeError, IndexError) as e:
            print(f"Error parsing item: {e}")

    return items

def scrape_page(page_number, config_key):
    """
    Scrapes a specific page number using the site configuration.
    
    Args:
        page_number (int): The page number to scrape.
        config_key (str): The key to identify the site configuration.
    
    Returns:
        list: A list of tuples containing parsed item data for the page.
    """
    config = SITE_CONFIGS[config_key]
    url = config['base_url'].format(page_number)
    html_content = fetch_page(url)
    if html_content:
        return parse_page(html_content, config)
    return []

def main():
    """
    Main function to coordinate the scraping process.
    """
    start_time = time.time()

    site = 'books'  # Change to 'quotes' for the other site
    all_items = []

    # Using ThreadPoolExecutor to scrape pages concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(scrape_page, i, site) for i in range(1, NUM_PAGES + 1)]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                all_items.extend(result)

    # Print results
    for item in all_items:
        if site == 'quotes':
            text, author, tags = item
            print(f"Quote: {text}")
            print(f"Author: {author}")
            print(f"Tags: {', '.join(tags)}")
        else:
            title, price, rating = item
            print(f"Title: {title}")
            print(f"Price: {price}")
            print(f"Rating: {rating}")
        print()

    print(f"Scraping completed in {time.time() - start_time:.2f} seconds.")

if __name__ == "__main__":
    main()
