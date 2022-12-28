import pandas as pd
import time

# French government api endpoint for national fuel data
API_ENDPOINT = "https://data.economie.gouv.fr/explore/dataset/prix-carburants-fichier-instantane-test-ods-copie" \
               "/download?format=csv&timezone=Europe/Berlin&use_labels_for_header=false "


# Function to fetch api data
def fetch_data():
    start = time.time()
    print("Fetching data...")
    res = pd.read_csv(API_ENDPOINT, delimiter=';')
    print("Data fetched in", time.time() - start, "seconds")

    # Getting context values
    fuel_list = pd.unique(res['prix_nom'].dropna())
    deps_list = pd.unique(res['dep_code'].dropna())
    deps_list = deps_list.astype('str')
    deps_list.sort()
    return {'data': res, 'fuels': fuel_list, 'deps': deps_list}


def query_builder(dataframe, filters):
    query = "True"
    if len(filters) == 0:
        return query

    for key in filters.keys():
        query += " and " + key + "=='" + str(filters[key]) + "'"

    return dataframe.query(query)
