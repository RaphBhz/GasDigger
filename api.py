from geopy.geocoders import Nominatim
import pandas as pd
import time

API_ENDPOINT = "data.csv"

def get_geo(adress):
    geolocator = Nominatim(user_agent="gasdigger")
    location = geolocator.geocode(adress, exactly_one=False)
    return location

def verif_adress(adress):
    try:
        geolocator = Nominatim(user_agent="adamfrancetest@gmail.com")
        location = geolocator.geocode(adress+', France', language="fr", exactly_one=False)
        print(location)
        time.sleep(1)
        return location
    except:
        print("Caught it!")
        time.sleep(1)
        return False

def fetch_data():
    start = time.time()
    print("Fetching data...")
    res = pd.read_csv(API_ENDPOINT, delimiter=';')
    print("Data fetched in", time.time() - start, "seconds")
    return res