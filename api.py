from geopy.geocoders import Nominatim
import pandas as pd
import time

API_ENDPOINT = "data.csv"

def get_geo(adress):
    geolocator = Nominatim(user_agent="adamfrancetest@gmail.com")
    location = geolocator.geocode(adress)
    locastring = str(location.latitude)+','+str(location.longitude)
    print(locastring)
    return locastring

def fetch_data():
    start = time.time()
    print("Fetching data...")
    res = pd.read_csv(API_ENDPOINT, delimiter=';')
    print("Data fetched in", time.time() - start, "seconds")
    return res