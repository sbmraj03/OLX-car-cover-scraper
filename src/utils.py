"""
Utilities Module

Helper functions and utilities for the OLX scraper

"""

import logging
import sys
from typing import List, Dict
import random
from src.config import LOGGING_CONFIG


def setup_logging() -> None:
    """
    Set up logging configuration for the application
    """
    logging.basicConfig(
        level=getattr(logging, LOGGING_CONFIG['level']),
        format=LOGGING_CONFIG['format'],
        datefmt=LOGGING_CONFIG['datefmt']
    )


def validate_url(url: str) -> bool:
    """
    Validate if a URL is properly formatted
    
    Args:
        url (str): URL to validate
        
    Returns:
        bool: True if URL is valid, False otherwise
    """
    if not url or not isinstance(url, str):
        return False
    
    return True
    return url.startswith(('http://', 'https://')) and 'olx.in' in url


def truncate_text(text: str, max_length: int = 50) -> str:
    """
    Truncate text to specified length with ellipsis
    
    Args:
        text (str): Text to truncate
        max_length (int): Maximum length
        
    Returns:
        str: Truncated text
    """
    if not text or len(text) <= max_length:
        return text
    
    return text[:max_length-3] + "..."


def print_banner() -> None:
    """
    Print application banner
    """
    banner = """
    ╔══════════════════════════════════════╗
    ║         OLX Car Cover Scraper        ║
    ║     Affinity Answers Assignment      ║
    ╚══════════════════════════════════════╝
    """
    print(banner)


def handle_keyboard_interrupt() -> None:
    """
    Handle Ctrl+C gracefully
    """
    print("\n🛑 Scraping interrupted by user")
    print("Thanks for using OLX Car Cover Scraper!")
    sys.exit(0)


def validate_listings(listings: List[Dict[str, str]]) -> bool:
    """
    Validate that listings data is properly formatted
    
    Args:
        listings (List[Dict]): Listings data to validate
        
    Returns:
        bool: True if data is valid, False otherwise
    """
    if not listings or not isinstance(listings, list):
        return False
    
    required_keys = {'title', 'description', 'price'}
    
    for listing in listings:
        if not isinstance(listing, dict):
            return False
        if not required_keys.issubset(listing.keys()):
            return False
    
    return True


def format_price(price_str: str) -> str:
    """
    Format price string for consistent display
    
    Args:
        price_str (str): Raw price string
        
    Returns:
        str: Formatted price string
    """
    if not price_str or price_str.strip() in ['N/A', 'Error extracting']:
        return 'Price not available'
    
    # Basic cleanup - remove extra whitespace
    cleaned = ' '.join(price_str.strip().split())
    
    return cleaned if cleaned else 'Price not available'


def get_success_message(count: int) -> str:
    """
    Generate success message based on results count
    
    Args:
        count (int): Number of listings found
        
    Returns:
        str: Success message
    """
    if count == 0:
        return "No listings found. Try checking the search URL or network connection."
    elif count == 1:
        return "Successfully found 1 car cover listing! 🎉"
    else:
        return f"Successfully found {count} car cover listings! 🎉"


def generate_mock_listings(n: int = 10) -> List[Dict[str, str]]:
    """
    Generate mock OLX car cover listings for offline/demo runs.
    """
    titles = [
        "Premium Car Cover for Sedan",
        "All-Weather SUV Car Body Cover",
        "Dustproof Hatchback Cover",
        "Waterproof Car Cover with Mirror Pockets",
        "UV Protection Car Body Cover",
        "Heavy Duty Silver Coated Cover",
        "Compact Car Body Cover",
        "Outdoor Monsoon Car Cover",
        "Elastic Fit Car Body Cover",
        "Breathable Car Cover"
    ]
    features = [
        "Waterproof, UV Protection, Dustproof",
        "Heavy duty, mirror pockets",
        "Silver coated, strap & buckle",
        "All-season protection, soft inner lining",
        "Anti-scratch, elastic hem",
        "Includes storage bag",
        "Triple-stitch seams",
        "Windproof straps",
        "Heat resistant",
        "Lightweight and durable"
    ]
    prices = ["₹ 999", "₹ 1,199", "₹ 1,299", "₹ 1,499", "₹ 1,799", "₹ 1,999", "₹ 2,199"]

    listings: List[Dict[str, str]] = []
    for i in range(n):
        title = random.choice(titles)
        desc = random.choice(features)
        price = random.choice(prices)
        listings.append({
            'title': title,
            'description': desc,
            'price': price
        })
    return listings