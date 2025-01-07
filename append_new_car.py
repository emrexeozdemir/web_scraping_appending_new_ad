from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QLabel, QVBoxLayout, QWidget
import sys
import threading
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import pandas as pd
import csv
from datetime import datetime


class ScraperApp(QMainWindow):
    def __init__(self):
        super(ScraperApp, self).__init__()

        self.setWindowTitle("Web Scraper GUI")
        self.setGeometry(200, 200, 600, 400)

        self.is_scraping = False

        # Main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Log output
        self.log_output = QTextEdit(self)
        self.log_output.setReadOnly(True)
        self.layout.addWidget(QLabel("Log Output:"))
        self.layout.addWidget(self.log_output)

        # Buttons
        self.start_button = QPushButton("Start Scraping", self)
        self.start_button.clicked.connect(self.start_scraping)
        self.layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop Scraping", self)
        self.stop_button.clicked.connect(self.stop_scraping)
        self.stop_button.setEnabled(False)
        self.layout.addWidget(self.stop_button)

        # Status label
        self.status_label = QLabel("Status: Idle", self)
        self.layout.addWidget(self.status_label)

        # Selenium driver
        self.driver = None
        self.counter = 0

    def log_message(self, message):
        self.log_output.append(message)

    def start_scraping(self):
        self.is_scraping = True
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.status_label.setText("Status: Scraping...")

        # Start scraping in a separate thread
        threading.Thread(target=self.run_scraper, daemon=True).start()

    def stop_scraping(self):
        self.is_scraping = False
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.status_label.setText("Status: Stopped")

        if self.driver:
            self.driver.quit()

    def wait_for_element_or_refresh(self, timeout, locator):
        """
        Waits for a specific element to appear within the given timeout.
        If the element is not found, refresh the page and retry.
        """
        for attempt in range(3):  # Retry up to 3 times
            try:
                # Wait for the element to be present
                WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located(locator)
                )
                return True  # Element found
            except TimeoutException:
                print(f"Attempt {attempt + 1}: Timeout waiting for element. Refreshing page.")
                self.driver.refresh()
        print("Element not found after 3 attempts. Skipping.")
        return False  # Element not found after retries

    def run_scraper(self):

        csv_file_path = "test.csv"
        df_existent = pd.read_csv(csv_file_path)

        columns = [
            "ad_Id", "ad_date", "ad_loc1", "ad_loc2", "brand", "series", "model", "year", "mileage",
            "transmission", "fuel_type", "body_type", "color", "engine_capacity", "engine_power",
            "drive_type", "vehicle_condition", "fuel_consumption", "fuel_tank", "paint/replacement",
            "trade_in", "seller_type", "seller_name", "ad_price", "ad_url"
        ]
        key_to_column = {
            "İlan No": "ad_Id",
            "İlan Tarihi": "ad_date",
            "Marka": "brand",
            "Seri": "series",
            "Model": "model",
            "Yıl": "year",
            "Kilometre": "mileage",
            "Vites Tipi": "transmission",
            "Yakıt Tipi": "fuel_type",
            "Kasa Tipi": "body_type",
            "Renk": "color",
            "Motor Hacmi": "engine_capacity",
            "Motor Gücü": "engine_power",
            "Çekiş": "drive_type",
            "Araç Durumu": "vehicle_condition",
            "Ortalama Yakıt Tüketimi": "fuel_consumption",
            "Yakıt Deposu": "fuel_tank",
            "Boya-değişen": "paint/replacement",
            "Takasa Uygun": "trade_in",
            "Kimden": "seller_type"
        }
        place_holder = "Unspecified"

        # Selenium setup
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        service = Service(executable="chromedriver.exe")
        self.driver = webdriver.Chrome(service=service, options=options)

        current_url = "https://www.arabam.com/ikinci-el/otomobil?sort=startedAt.desc&take=50"

        try:
            for index_page in range(49):
                if not self.is_scraping:
                    break

                self.log_message(f"Navigating to page {index_page + 1}")
                current_url_2 = current_url + f"&page={index_page + 1}"
                self.driver.get(current_url_2)

                # Wait for listings to load
                WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "tr.listing-list-item.should-hover.bg-white"))
                )

                car_list = self.driver.find_elements(By.CSS_SELECTOR, "tr.listing-list-item.should-hover.bg-white")
                for car in car_list:
                    if self.counter >= 10:
                        self.stop_scraping()
                        self.log_message("There are no more new ads. Closing the program...")
                    if not self.is_scraping:
                        break

                    car_url = car.find_element(By.TAG_NAME, 'a').get_attribute('href')
                    self.log_message(f"Processing car URL: {car_url}")

                    # Open car detail page
                    self.driver.execute_script("window.open(arguments[0]);", car_url)
                    self.driver.switch_to.window(self.driver.window_handles[-1])

                    # Process data (mock example)
                    ad_data = {column: None for column in columns}
                    if not self.wait_for_element_or_refresh(30, (By.CSS_SELECTOR, ".property-item")):
                        continue
                    property_items = self.driver.find_elements(By.CSS_SELECTOR, ".property-item")
                    for item in property_items:
                        try:
                            key = item.find_element(By.CSS_SELECTOR, ".property-key").text.strip()
                            value_element = item.find_element(By.CSS_SELECTOR, ".property-value")
                            value = value_element.text.strip()
                            column_name = key_to_column.get(key)  # Use the mapping
                            if column_name:
                                ad_data[column_name] = value

                        except Exception as e:
                            print(f"Error processing property item: {e}")
                        try:
                            ad_loc = self.driver.find_element(By.CSS_SELECTOR, '.product-location').text
                            loc1, loc2 = ad_loc.split(",")
                            ad_data["ad_loc1"] = loc1
                            ad_data["ad_loc2"] = loc2

                        except Exception as e:
                            continue
                        ad_data["seller_name"] = self.driver.find_element(By.CSS_SELECTOR,
                                                                          ".advert-owner-name").text.strip()
                        ad_data["ad_price"] = self.driver.find_element(By.XPATH,
                                                                       '//*[@data-testid="desktop-information-price"]').text.strip()
                        ad_data["ad_url"] = car_url

                    processed_data = [ad_data[column] if ad_data[column] is not None else place_holder for column in
                                      columns]
                    processed_data_df = pd.DataFrame([processed_data], columns=columns)

                    # Ensure all columns are the same type (string)
                    df_existent['ad_Id'] = df_existent['ad_Id'].astype(str)
                    processed_data_df['ad_Id'] = processed_data_df['ad_Id'].astype(str)

                    # Check for duplicates based on 'ad_Id'
                    if processed_data_df['ad_Id'].iloc[0] not in df_existent['ad_Id'].values:
                        with open(csv_file_path, mode="a", newline="", encoding="utf-8-sig") as csvfile:
                            writer = csv.writer(csvfile)
                            writer.writerow(processed_data)
                        self.log_message("New data added.")
                    else:
                        self.log_message("Data already exists. Skipping.")
                        self.counter += 1

                    self.driver.close()
                    self.driver.switch_to.window(self.driver.window_handles[0])

        except Exception as e:
            self.log_message(f"Error occurred: {e}")

        self.stop_scraping()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    scraper_app = ScraperApp()
    scraper_app.show()
    sys.exit(app.exec_())
