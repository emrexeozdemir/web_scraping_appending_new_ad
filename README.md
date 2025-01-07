# Web Scraper with PyQt5 GUI

This project is a Python-based web scraper with a graphical user interface (GUI) built using PyQt5. It scrapes automobile listings from a specific website, checks for new data, and appends only new entries to an existing CSV file.

## Features

- **User-Friendly GUI:**
  - Start and stop scraping with buttons.
  - Display real-time logs in the GUI.
  - Show scraping status.

- **Data Handling:**
  - Reads existing data from a CSV file.
  - Scrapes listing details from a target website.
  - Appends only new data to the CSV file, avoiding duplicates.

- **Selenium Integration:**
  - Uses Selenium WebDriver for dynamic web scraping.
  - Includes robust error handling and retries for missing elements.

## Requirements

- Python 3.8 or later
- Google Chrome browser
- [ChromeDriver](https://sites.google.com/chromium.org/driver/) (compatible with your Chrome version)

### Python Libraries

Install the required libraries using pip:
```bash
pip install PyQt5 selenium pandas
```

## How It Works

1. **Initialization:**
   - Reads existing data from `test.csv`.
   - Sets up a mapping between website data fields and CSV columns.

2. **Scraping:**
   - Navigates through multiple pages of listings.
   - Opens each listing and extracts details such as ad ID, price, location, seller information, and more.

3. **Data Processing:**
   - Checks for duplicates using the `ad_Id` field.
   - Appends new data to `test.csv`.

4. **GUI Interaction:**
   - Provides start/stop buttons for scraping.
   - Displays logs and status updates in real time.

## Usage

1. **Run the Program:**
   ```bash
   python append_new_car_last.py
   ```

2. **Start Scraping:**
   - Click the "Start Scraping" button.

3. **Stop Scraping:**
   - Click the "Stop Scraping" button at any time.

4. **View Logs:**
   - Monitor progress in the "Log Output" section of the GUI.

## CSV File Structure

The scraper outputs data to `test.csv` with the following columns:

| Column Name            | Description                     |
|------------------------|---------------------------------|
| ad_Id                 | Unique ID for the ad           |
| ad_date               | Date of the ad                 |
| ad_loc1               | Primary location               |
| ad_loc2               | Secondary location             |
| brand                 | Vehicle brand                  |
| series                | Vehicle series                 |
| model                 | Vehicle model                  |
| year                  | Year of manufacture            |
| mileage               | Mileage of the vehicle         |
| transmission          | Transmission type              |
| fuel_type             | Type of fuel                   |
| body_type             | Body type of the vehicle       |
| color                 | Vehicle color                  |
| engine_capacity       | Engine capacity                |
| engine_power          | Engine power                   |
| drive_type            | Drive type (e.g., FWD, AWD)    |
| vehicle_condition     | Condition of the vehicle       |
| fuel_consumption      | Fuel consumption rate          |
| fuel_tank             | Fuel tank capacity             |
| paint/replacement     | Paint/replacement status       |
| trade_in              | Trade-in option                |
| seller_type           | Type of seller (e.g., dealer)  |
| seller_name           | Seller's name                  |
| ad_price              | Price of the listing           |
| ad_url                | URL of the ad                  |

## Notes

- Ensure `chromedriver.exe` is in the project directory or accessible via PATH.
- The scraper retries up to 3 times for missing elements before skipping.
- Modify `csv_file_path` in the code if you want to use a different file name or location.

## Limitations

- Hardcoded for a specific website.
- Requires adjustments for other websites with different structures.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
