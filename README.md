
# Target Product Scraper

This project is a web scraper designed to extract product information from Target's website, focusing on promotional deals and volume discounts.


## Features

- Asynchronous scraping of product data from Target's website
- Extraction of promotional deals and volume discounts
- Category-based scraping
- Apply promotional deals and volume discounts
- CSV output of processed product data

## Requirements

- Python 3.11
- aiohttp
- asyncio
- concurrent.futures
- logging

## Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/AlbinAimleap/target.git
   cd target
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the main script:
   ```bash
   python main.py
   ```
   

## Configuration

- Modify the `CATEGORIES` list in `main.py` to specify which categories to scrape.
- Adjust logging levels in `main.py` as needed.

## Output

The script will generate CSV files containing the processed product data, including promotional deals and volume discounts.

