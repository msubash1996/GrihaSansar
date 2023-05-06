import time
import requests
import pandas as pd
  
# api-endpoint 
BASE_URL = "https://www.nepalhomes.com"

def getData(page=1):
    FULL_URL = f"{BASE_URL}/api/property/public/data?sort=1&page={page}&find_property_category=5d660cb27682d03f547a6c4a&size=8&find_property_purpose=5db2bdb42485621618ecdae6"

    r = requests.get(url = FULL_URL)
    data = r.json()

    return data

list_infos = getData()
total_listings = list_infos["totaldata"]
size = list_infos["size"]
total_pages = int(total_listings / size) + 1
sleep_time = 2

all_data = []

for page in range(1, total_pages+1):
    if ( page % 15 == 0 ):
        time.sleep(sleep_time)
        print(f"Sleeping for {sleep_time} seconds")
    print(f"Getting Data ... Page {page}/{total_pages}")
    data = getData(page)
    all_data += data["data"]

df = pd.DataFrame(all_data)
df.to_csv("data.csv")
print("Data saved as data.csv")