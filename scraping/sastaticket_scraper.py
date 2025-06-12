from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import time

def scrape_sastaticket_hotels():
    options = Options()
    #options.add_argument("--headless")  # Run in background
    driver = webdriver.Chrome(options=options)

    base_url = "https://www.sastaticket.pk/hotels"
    driver.get(base_url)
    time.sleep(3)

    hotels = []

    # NOTE: You’ll update this with actual selectors and loop later
    hotel_elements = driver.find_elements(By.CLASS_NAME, "hotel-card")  # placeholder
    for hotel in hotel_elements:
        name = hotel.find_element(By.CLASS_NAME, "hotel-name").text
        city = hotel.find_element(By.CLASS_NAME, "hotel-location").text
        price = hotel.find_element(By.CLASS_NAME, "price").text
        hotels.append({
            "name": name,
            "city": city,
            "price": price,
        })

    driver.quit()

    df = pd.DataFrame(hotels)
    df.to_csv("data/sastaticket_hotels.csv", index=False)
    print("✅ Hotel data saved to data/sastaticket_hotels.csv")

if __name__ == "__main__":
    scrape_sastaticket_hotels()

