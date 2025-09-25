"""
Data Processing Module

Functions for processing, displaying and saving scraped data

"""

import pandas as pd
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


def display_results_table(listings: List[Dict[str, str]]) -> None:
    """
    Display results in a formatted table
    
    Args:
        listings (List[Dict]): List of listing dictionaries
    """
    if not listings:
        print("No listings found!")
        return
    
    # Create DataFrame for better table display
    df = pd.DataFrame(listings)
    
    # Set pandas display options for better formatting
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', 50)
    
    print(f"\n{'='*80}")
    print(f"FOUND {len(listings)} CAR COVER LISTINGS ON OLX")
    print(f"{'='*80}")
    print(df.to_string(index=True))
    print(f"{'='*80}\n")


def save_to_csv(listings: List[Dict[str, str]], filename: str = "olx_car_covers.csv") -> None:
    """
    Save results to CSV file
    
    Args:
        listings (List[Dict]): List of listing dictionaries
        filename (str): Output filename
    """
    if listings:
        df = pd.DataFrame(listings)
        df.to_csv(filename, index=False, encoding='utf-8')
        logger.info(f"Results saved to {filename}")
        print(f"📄 Data saved to {filename}")
    else:
        logger.warning("No data to save")


def clean_price_data(listings: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    Clean and standardize price data
    
    Args:
        listings (List[Dict]): Raw listing data
        
    Returns:
        List[Dict]: Cleaned listing data
    """
    cleaned_listings = []
    
    for listing in listings:
        cleaned_listing = listing.copy()
        
        # Clean price field - remove extra whitespace, standardize format
        price = listing.get('price', '').strip()
        if price and price != "N/A":
            # Remove multiple spaces and clean up
            cleaned_listing['price'] = ' '.join(price.split())
        
        # Clean title and description
        cleaned_listing['title'] = listing.get('title', '').strip()
        cleaned_listing['description'] = listing.get('description', '').strip()
        
        cleaned_listings.append(cleaned_listing)
    
    return cleaned_listings


def filter_valid_listings(listings: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    Filter out invalid or incomplete listings
    
    Args:
        listings (List[Dict]): Raw listing data
        
    Returns:
        List[Dict]: Filtered valid listings
    """
    valid_listings = []
    
    for listing in listings:
        # Check if listing has essential data
        if (listing.get('title') and 
            listing.get('title') not in ['N/A', 'Error extracting'] and
            len(listing.get('title', '')) > 5):  # Title should be meaningful
            
            valid_listings.append(listing)
    
    logger.info(f"Filtered {len(valid_listings)} valid listings from {len(listings)} total")
    return valid_listings


def generate_summary_stats(listings: List[Dict[str, str]]) -> None:
    """
    Generate and display summary statistics
    
    Args:
        listings (List[Dict]): Listing data
    """
    if not listings:
        return
    
    total_listings = len(listings)
    listings_with_price = len([l for l in listings if l.get('price') and l['price'] not in ['N/A', 'Error extracting']])
    listings_with_description = len([l for l in listings if l.get('description') and l['description'] not in ['N/A', 'Error extracting']])
    
    print(f"\n📊 SUMMARY STATISTICS")
    print(f"{'='*40}")
    print(f"Total listings found: {total_listings}")
    print(f"Listings with price: {listings_with_price}")
    print(f"Listings with description: {listings_with_description}")
    print(f"Data completeness: {(listings_with_price/total_listings)*100:.1f}%")
    print(f"{'='*40}\n")