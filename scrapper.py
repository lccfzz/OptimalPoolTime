# %%
import requests
import csv
import datetime
import time
import re
from bs4 import BeautifulSoup

def is_scraping_time():
    now = datetime.datetime.now()
    hour, minute = now.hour, now.minute
    weekday = now.weekday()  # Monday = 0, Sunday = 6
    
    if weekday < 5:  # Monday to Friday
        return 5 <= hour < 23
    else:  # Saturday, Sunday
        return 9 <= hour < 23

def scrape_data():
    url = "https://www.sutka.eu"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch data: {response.status_code}")
        return None
    
    soup = BeautifulSoup(response.text, "html.parser")
    header_info = soup.find("div", class_="header-info")
    if not header_info:
        print("Failed to find data.")
        return None
    
    try:
        text = header_info.get_text(" ", strip=True)
        numbers = re.findall(r"\d+", text)
        
        if len(numbers) < 3:
            print("Unexpected data format.")
            return None

        occupancy, pool_guests, waterpark_guests = map(int, numbers[:3])
        return [
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
            pool_guests, 
            waterpark_guests, 
            occupancy
        ]
    except Exception as e:
        print(f"Error parsing data: {e}")
        return None
    
data_collection = []

while True:
    if is_scraping_time():
        record = scrape_data()
        if record:
            data_collection.append(record)
            print(f"Data recorded: {record}")
    
    now = datetime.datetime.now()
    if now.hour == 22 and now.minute == 1:
        with open('data.csv', "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(data_collection)
        print(f"Data saved to data.csv")
        data_collection = []
    
    time.sleep(30)

    if now.hour == 22 and now.minute == 1:
        break

# %%

# %%
