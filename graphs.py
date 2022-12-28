import plotly.express as px
import api


def create_histogram(dataframe, fuel, dep, target):
    # Returning an empty figure if there is no data
    if dataframe is None:
        return {}
    # Ensuring that filters exist by setting default values
    if fuel is None:
        fuel = 'E10'
    if dep is None:
        dep = 94
    # Getting filtered data matching the given fuel and department
    filters = {"prix_nom": fuel, "dep_code": dep}
    data = api.query_builder(dataframe, filters)[target]
    max_value = data.max()
    min_value = data.min()

    # Preparing the graph
    return px.histogram(data,
                        x=target,
                        labels={'prix_valeur': 'Prix (€)', 'count': 'Stations (unité)'},
                        range_x=[min_value, max_value],
                        nbins=50,
                        histnorm='density'
                        )
