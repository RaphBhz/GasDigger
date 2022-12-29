from geopy.geocoders import Nominatim
import pandas as pd
import time

<<<<<<< Updated upstream
# French government api endpoint for national fuel data
API_ENDPOINT = "https://data.economie.gouv.fr/explore/dataset/prix-carburants-fichier-instantane-test-ods-copie/download?format=csv&timezone=Europe/Berlin&use_labels_for_header=false"
=======
API_ENDPOINT = "data.csv"

def get_geo(adress):
    geolocator = Nominatim(user_agent="adamfrancetest@gmail.com")
    location = geolocator.geocode(adress)
    locastring = str(location.latitude)+','+str(location.longitude)
    print(locastring)
    return locastring
>>>>>>> Stashed changes

def fetch_data():
    start = time.time()
    print("Fetching data...")
    res = pd.read_csv(API_ENDPOINT, delimiter=';')
    print("Data fetched in", time.time() - start, "seconds")
<<<<<<< Updated upstream
    return res
=======
    return res
>>>>>>> Stashed changes
