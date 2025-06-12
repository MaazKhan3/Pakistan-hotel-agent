# scraper/booking_scraper.py

import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def init_driver():
    options = Options()
    # Headless mode disabled so you can see the browser
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    driver = webdriver.Chrome(options=options)
    return driver


def scrape_booking(city: str, max_pages: int = 1, delay: int = 5):
    """
    Scrapes Booking.com for hotel data in a given city.
    :param city: City name (e.g., 'Skardu')
    :param max_pages: Number of pages to scrape
    :param delay: Delay (in seconds) to allow page to load
    :return: DataFrame with hotel data
    """
    driver = init_driver()
    base_url = f"https://www.booking.com/searchresults.html?ss={city}&rows=25"
    hotels = []

    for page in range(max_pages):
        url = base_url + f"&offset={page * 25}"
        print(f"[+] Scraping page {page+1}: {url}")
        driver.get(url)
        time.sleep(delay)

        listings = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='property-card']")

        for hotel in listings:
            try:
                name = hotel.find_element(By.CSS_SELECTOR, "div[data-testid='title']").text
                location = hotel.find_element(By.CSS_SELECTOR, "span[data-testid='address']").text
                url = hotel.find_element(By.TAG_NAME, "a").get_attribute("href")

                try:
                    price = hotel.find_element(By.CSS_SELECTOR, "span[data-testid='price-and-discounted-price']").text
                except:
                    price = "N/A"

                try:
                    rating = hotel.find_element(By.CSS_SELECTOR, "div[data-testid='review-score'] > div").text
                except:
                    rating = "N/A"

                hotels.append({
                    "hotel_name": name,
                    "location": location,
                    "price": price,
                    "rating": rating,
                    "url": url,
                    "city": city
                })
            except Exception as e:
                print(f"[!] Skipped one listing due to: {e}")

    driver.quit()

    df = pd.DataFrame(hotels)
    os.makedirs("data", exist_ok=True)
    filename = f"data/{city.lower().replace(' ', '_')}_hotels.csv"
    df.to_csv(filename, index=False)
    print(f"[✓] Scraped {len(df)} hotels. Data saved to: {filename}")
    return df


if __name__ == "__main__":
    # Example usage
    scrape_booking("Skardu", max_pages=1)
