"""
Configuration Module

Contains all configuration settings for the OLX scraper

"""

# Base URL for OLX website
BASE_URL = "https://www.olx.in"

# Default search URL for car covers
DEFAULT_SEARCH_URL = "https://www.ebay.com/sch/i.html?_nkw=car+cover"

# HTTP Headers to mimic a real browser
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
}

# Scraping settings
MAX_PAGES_DEFAULT = 2
REQUEST_DELAY = 2  # seconds between requests
TIMEOUT = 10  # seconds for HTTP requests

# Output settings
OUTPUT_CSV_FILE = "olx_car_covers.csv"
MAX_DESCRIPTION_LENGTH = 100  # for display purposes

# CSS Selectors for OLX elements (may need updates if OLX changes their structure)
SELECTORS = {
    'listing_containers': [
        'div[data-aut-id="itemBox"]',
        'div.EIR5N',
        'li[data-aut-id="itemBox"]'
    ],
    'title': 'span[data-aut-id="itemTitle"]',
    'description': 'span[data-aut-id="itemDescription"]',
    'price': 'span[data-aut-id="itemPrice"]'
}

# Logging configuration
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'datefmt': '%Y-%m-%d %H:%M:%S'
}