"""
OLX Scraper Module

Contains the main OLXScraper class for scraping car cover listings from OLX.in

"""

import requests
from bs4 import BeautifulSoup
import time
from typing import List, Dict, Optional
import logging
from src.utils import setup_logging
from src.config import HEADERS, BASE_URL, REQUEST_DELAY

logger = logging.getLogger(__name__)


class OLXScraper:
    """
    A class to scrape OLX search results for car covers
    """
    
    def __init__(self, base_url: str = BASE_URL):
        """
        Initialize the scraper with base URL and headers
        
        Args:
            base_url (str): Base URL for OLX website
        """
        self.base_url = base_url
        self.headers = HEADERS
        setup_logging()
        
    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """
        Fetch and parse a web page
        
        Args:
            url (str): URL to fetch
            
        Returns:
            BeautifulSoup object or None if failed
        """
        try:
            logger.info(f"Fetching URL: {url}")
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup
            
        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
            return None
    
    def extract_listing_data(self, listing_element) -> Dict[str, str]:
        """
        Extract data from a single listing element
        
        Args:
            listing_element: BeautifulSoup element containing listing data
            
        Returns:
            Dictionary with title, description, and price
        """
        try:
            # Extract title
            title_elem = listing_element.find('span', {'data-aut-id': 'itemTitle'})
            title = title_elem.get_text(strip=True) if title_elem else "N/A"
            
            # Extract description
            desc_elem = listing_element.find('span', {'data-aut-id': 'itemDescription'})
            description = desc_elem.get_text(strip=True) if desc_elem else "N/A"
            
            # Extract price
            price_elem = listing_element.find('span', {'data-aut-id': 'itemPrice'})
            price = price_elem.get_text(strip=True) if price_elem else "N/A"
            
            return {
                'title': title,
                'description': description,
                'price': price
            }
            
        except Exception as e:
            logger.warning(f"Error extracting listing data: {e}")
            return {
                'title': "Error extracting",
                'description': "Error extracting", 
                'price': "Error extracting"
            }
    
    def scrape_search_results(self, search_url: str, max_pages: int = 3) -> List[Dict[str, str]]:
        """
        Scrape search results from OLX
        
        Args:
            search_url (str): Search URL to scrape
            max_pages (int): Maximum number of pages to scrape
            
        Returns:
            List of dictionaries containing listing data
        """
        all_listings = []
        current_page = 1
        
        while current_page <= max_pages:
            # Construct page URL
            if current_page == 1:
                page_url = search_url
            else:
                # Add page parameter to URL
                separator = "&" if "?" in search_url else "?"
                page_url = f"{search_url}{separator}page={current_page}"
            
            soup = self.fetch_page(page_url)
            if not soup:
                logger.error(f"Failed to fetch page {current_page}")
                break
            
            # Find all listing containers - try multiple selectors
            listings = (
                soup.find_all('div', {'data-aut-id': 'itemBox'}) or
                soup.find_all('div', class_=lambda x: x and 'EIR5N' in str(x)) or
                soup.find_all('li', {'data-aut-id': 'itemBox'})
            )
            
            if not listings:
                logger.warning(f"No listings found on page {current_page}")
                break
                
            logger.info(f"Found {len(listings)} listings on page {current_page}")
            
            # Extract data from each listing
            page_listings = []
            for listing in listings:
                listing_data = self.extract_listing_data(listing)
                if listing_data['title'] != "N/A":  # Only add if we got valid data
                    page_listings.append(listing_data)
            
            all_listings.extend(page_listings)
            logger.info(f"Extracted {len(page_listings)} valid listings from page {current_page}")
            
            current_page += 1
            
            # Be respectful to the server
            time.sleep(REQUEST_DELAY)
        
        return all_listings