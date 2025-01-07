# Web Scraping New Ads for arabam.com

This project uses Selenium to scrape advertisements for used cars from [arabam.com](https://www.arabam.com). The script is designed to check for new ads and append them to an existing CSV file while avoiding duplicates. This ensures that only fresh data is collected without reprocessing already scraped ads.

## Features

- Scrapes car advertisements from arabam.com.
- Identifies and appends only new ads to the existing dataset.
- Efficiently handles pagination and retries for network errors or page timeouts.
- Extracts detailed ad information, such as:
  - Advertisement ID
  - Date
  - Location
  - Brand, Series, and Model
  - Year, Mileage, Transmission, and Fuel Type
  - Seller details and price

## Prerequisites

- Python 3.x
- Google Chrome browser
- ChromeDriver (compatible with your Chrome version)
- Required Python packages:
  - `selenium`
  - `pandas`
  - `datetime`

Install the required packages using pip:
```bash
pip install selenium pandas
```

## How It Works

1. **Initialization:**
   - The script reads existing data from a CSV file (`test.csv`) into a Pandas DataFrame (`df_existent`).
   - Sets up Selenium WebDriver in headless mode for efficient scraping.

2. **Fetching Advertisements:**
   - Navigates to the arabam.com listing page for used cars.
   - Iterates through multiple pages (up to a maximum of 49 pages) and fetches car ad links.

3. **Processing Individual Ads:**
   - For each ad, the script opens its page, extracts detailed information, and maps it to predefined columns.
   - Checks if the `ad_Id` already exists in the existing dataset.
   - If the ad is new, appends its data to the CSV file; otherwise, skips it.

4. **Error Handling:**
   - Implements retry logic to handle network timeouts or missing elements.
   - Skips ads or pages that cannot be processed after several attempts.

5. **Output:**
   - A CSV file (`test.csv`) that contains all the scraped data, including new ads.

## Key Functions

- `wait_for_element_or_refresh(driver, timeout, locator)`:
  Ensures the presence of required elements on the page by retrying after refreshing the page.

- **Mapping of ad details:**
  The script uses a dictionary (`key_to_column`) to map ad properties (e.g., "İlan No") to specific column names (e.g., `ad_Id`).

## Usage

1. Ensure that `chromedriver.exe` is in the same directory as the script or update the path in the `Service` initialization.
2. Place the existing dataset (`test.csv`) in the script directory or update the `csv_file_path` variable.
3. Run the script:
   ```bash
   python append_new_car.py
   ```
4. The script will append new ads to the CSV file while avoiding duplicates.

## Notes

- The script limits duplicate checks to `ad_Id`. Ensure that the existing dataset has this column populated correctly.
- For testing or debugging, you can disable headless mode by removing the `--headless` argument from `ChromeOptions`.
- Adjust page limits or retry counts as needed based on your requirements or system constraints.

## Limitations

- The script assumes a maximum of 49 pages. Modify the range as needed for larger datasets.
- arabam.com layout or structure changes may require updates to the CSS selectors or XPath expressions.

## Disclaimer

This script is intended for educational and personal use only. Please ensure compliance with arabam.com's terms of service before using it for scraping.
