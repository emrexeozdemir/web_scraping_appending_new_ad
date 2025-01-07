from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import time
import csv
import time
from datetime import datetime
import pandas as pd

csv_file_path = "test.csv"

df_existent = pd.read_csv(csv_file_path)

count = 0
place_holder = "Unspecified"
start_time = datetime.now()

columns = [
    "ad_Id",
    "ad_date",
    "ad_loc1",
    "ad_loc2",
    "brand",
    "series",
    "model",
    "year",
    "mileage",
    "transmission",
    "fuel_type",
    "body_type",
    "color",
    "engine_capacity",
    "engine_power",
    "drive_type",
    "vehicle_condition",
    "fuel_consumption",
    "fuel_tank",
    "paint/replacement",
    "trade_in",
    "seller_type",
    "seller_name",
    "ad_price",
    "ad_url"
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


def wait_for_element_or_refresh(driver, timeout, locator):
    """
    Waits for a specific element to appear within the given timeout.
    If the element is not found, refresh the page and retry.
    """
    for attempt in range(3):  # Retry up to 3 times
        try:
            # Wait for the element to be present
            WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True  # Element found
        except TimeoutException:
            print(f"Attempt {attempt + 1}: Timeout waiting for element. Refreshing page.")
            driver.refresh()
    print("Element not found after 3 attempts. Skipping.")
    return False  # Element not found after retries

options = webdriver.ChromeOptions()
options.add_argument('--headless')
service = Service(executable="chromedriver.exe")
driver = webdriver.Chrome(service=service,options=options)


current_url ="https://www.arabam.com/ikinci-el/otomobil?sort=startedAt.desc&take=50"
driver.get(current_url)

for index_page in range(49):
    if count >= 10:
        print("There are no more new ads. Closing the program...")
        break
    print("index page: ", index_page)
    current_url_2 = current_url + f"&page={index_page + 1}"
    bol = False
    for attempt in range(3):
        try:
            driver.get(current_url_2)
            bol = True
        except TimeoutException:
            driver.refresh()
    if not bol:
        continue
    if not wait_for_element_or_refresh(driver, 30, (
    By.CSS_SELECTOR, "tr[class='listing-list-item should-hover bg-white']")):
        continue  # Skip this page if the element was not found
    car_list = driver.find_elements(By.CSS_SELECTOR, "tr[class='listing-list-item should-hover bg-white']")
    for index_ad in range(len(car_list)):
        car_url = car_list[index_ad].find_element(By.TAG_NAME, 'a').get_attribute('href')
        driver.execute_script("window.open(arguments[0]);", car_url)
        driver.switch_to.window(driver.window_handles[-1])

        ad_data = {column: None for column in columns}
        if not wait_for_element_or_refresh(driver, 30, (By.CSS_SELECTOR, ".property-item")):
            continue  # Skip this page if the element was not found
        property_items = driver.find_elements(By.CSS_SELECTOR, ".property-item")
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
                ad_loc = driver.find_element(By.CSS_SELECTOR, '.product-location').text
                loc1, loc2 = ad_loc.split(",")
                ad_data["ad_loc1"] = loc1
                ad_data["ad_loc2"] = loc2

            except Exception as e:
                continue
            ad_data["seller_name"] = driver.find_element(By.CSS_SELECTOR, ".advert-owner-name").text.strip()
            ad_data["ad_price"] = driver.find_element(By.XPATH,
                                                      '//*[@data-testid="desktop-information-price"]').text.strip()
            ad_data["ad_url"] = car_url
        print(ad_data)
        processed_data = [ad_data[column] if ad_data[column] is not None else place_holder for column in
                          columns]
        processed_data_df = pd.DataFrame([processed_data])

        if ad_data["ad_Id"] in df_existent["ad_Id"].values:
            print("Data already exists. Skipping.")
            count += 1
        else:
            with open(csv_file_path, mode="a", newline="", encoding="utf-8-sig") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(processed_data)
            print("New data added.")
        current_time = datetime.now()
        print(current_time - start_time)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
