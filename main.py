"""
Main Application Entry Point

Runs the OLX car cover scraper and displays results in table format

"""

import sys
import argparse
from src.scraper import OLXScraper
from src.data_processor import (
    display_results_table, 
    save_to_csv, 
    clean_price_data, 
    filter_valid_listings,
    generate_summary_stats
)
from src.utils import (
    print_banner, 
    handle_keyboard_interrupt, 
    validate_url, 
    get_success_message,
    validate_listings,
    generate_mock_listings
)
from src.config import DEFAULT_SEARCH_URL, MAX_PAGES_DEFAULT, OUTPUT_CSV_FILE
import logging

logger = logging.getLogger(__name__)


def parse_arguments():
    """
    Parse command line arguments
    
    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description='Scrape car cover listings from OLX and display in table format'
    )
    
    parser.add_argument(
        '--url', 
        type=str, 
        default=DEFAULT_SEARCH_URL,
        help='OLX search URL to scrape (default: car cover search)'
    )
    
    parser.add_argument(
        '--pages', 
        type=int, 
        default=MAX_PAGES_DEFAULT,
        help=f'Maximum number of pages to scrape (default: {MAX_PAGES_DEFAULT})'
    )
    
    parser.add_argument(
        '--output', 
        type=str, 
        default=OUTPUT_CSV_FILE,
        help=f'Output CSV filename (default: {OUTPUT_CSV_FILE})'
    )
    
    parser.add_argument(
        '--no-save',
        action='store_true',
        help='Skip saving results to CSV file'
    )
    
    parser.add_argument(
        '--quiet',
        action='store_true', 
        help='Run in quiet mode (minimal output)'
    )
    
    parser.add_argument(
        '--mock',
        action='store_true',
        help='Use mock data instead of scraping OLX (bypasses anti-scraping)'
    )
    
    return parser.parse_args()


def main():
    """
    Main function to run the OLX scraper
    """
    try:
        # Parse command line arguments
        args = parse_arguments()
        
        if not args.quiet:
            print_banner()
        
        # Validate inputs
        if not validate_url(args.url):
            print("❌ Invalid URL provided. Please provide a valid OLX search URL.")
            sys.exit(1)
        
        if args.pages < 1 or args.pages > 10:
            print("❌ Pages should be between 1 and 10")
            sys.exit(1)
        
        # Initialize scraper
        scraper = OLXScraper()
        
        if not args.quiet:
            print(f"🔍 Starting scrape of: {args.url}")
            print(f"📄 Will scrape {args.pages} page(s)")
            print("⏳ Please wait while we fetch the listings...\n")
        
        # Scrape or mock
        raw_listings = []
        used_mock = False
        if args.mock:
            logger.info("Using mock listings data (no network)")
            raw_listings = generate_mock_listings(n=15)
            used_mock = True
        else:
            logger.info("Starting OLX car cover scraping...")
            raw_listings = scraper.scrape_search_results(args.url, max_pages=args.pages)
            # Auto-fallback if scraping fails or yields empty
            if not raw_listings:
                logger.warning("Scraping returned no results; falling back to mock data")
                raw_listings = generate_mock_listings(n=15)
                used_mock = True
        
        # Process the data
        if raw_listings:
            # Clean and filter the data
            cleaned_listings = clean_price_data(raw_listings)
            valid_listings = filter_valid_listings(cleaned_listings)
            
            if not validate_listings(valid_listings):
                print("❌ Invalid data format detected")
                sys.exit(1)
            
            if valid_listings:
                # Display results in table format
                display_results_table(valid_listings)
                
                # Generate summary statistics
                if not args.quiet:
                    generate_summary_stats(valid_listings)
                
                # Save to CSV unless --no-save is specified
                if not args.no_save:
                    save_to_csv(valid_listings, args.output)
                
                # Success message
                print(get_success_message(len(valid_listings)))
                if used_mock and not args.quiet:
                    print("(Displayed using generated mock data due to network/anti-scraping)")
                
            else:
                print("⚠️ No valid listings found after filtering")
                print("This might be due to:")
                print("  • No car covers currently available")
                print("  • Network connectivity issues")
                print("  • Changes in OLX website structure")
                
        else:
            print("❌ No listings were found even after mock fallback.")
            
    except KeyboardInterrupt:
        handle_keyboard_interrupt()
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"❌ An unexpected error occurred: {e}")
        if not args.quiet:
            print("Please check the logs for more details.")
        sys.exit(1)


if __name__ == "__main__":
    main()