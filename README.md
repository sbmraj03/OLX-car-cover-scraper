# OLX Car Cover Scraper

Simple Python script that prints OLX car cover listings (title, description, price) in a table. If scraping is blocked, it automatically shows realistic mock results so you still get the table/CSV.

## Install

```bash
pip install -r requirements.txt
```

## Use

```bash
# basic
python main.py

# common options
python main.py --pages 2                 # scrape more pages
python main.py --output olx_car_covers.csv  # save CSV
python main.py --mock                    # force mock data only
```

That’s it. Real scrape first; if it fails, mock is shown in the same format.

## What it does

- Targets OLX search: `https://www.olx.in/items/q-car-cover?isSearchCall=true`
- Extracts: title, description, price (images intentionally ignored)
- Displays a clean table in the console and can save a CSV
- Handles timeouts/anti-scraping gracefully with an automatic mock fallback

## Output

- Console table of listings
- Optional CSV at `olx_car_covers.csv` (omit with `--no-save`)

## Project structure

- `main.py` — CLI entry; orchestrates scraping, processing, fallback
- `src/scraper.py` — fetch + parse OLX search pages
- `src/data_processor.py` — table display, CSV save, basic cleaning
- `src/utils.py` — logging, validation, mock data generator
- `src/config.py` — headers, defaults, simple settings

## Notes

- The script attempts real scraping first. If OLX blocks/changes layout, it auto-falls back to realistic mock data so the flow still demonstrates the expected output and CSV.
- Change defaults (headers, delays, URL) in `src/config.py` if needed.