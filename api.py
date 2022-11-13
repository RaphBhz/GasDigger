import pandas as pd
import time

# French government api endpoint for national fuel data
API_ENDPOINT = "https://data.economie.gouv.fr/explore/dataset/prix-carburants-fichier-instantane-test-ods-copie/download?format=csv&timezone=Europe/Berlin&use_labels_for_header=false"

# Function to fetch api data
def fetch_data():
    start = time.time()
    print("Fetching data...")
    res = pd.read_csv(API_ENDPOINT, delimiter=';')
    print("Data fetched in", time.time() - start, "seconds")
    return res
