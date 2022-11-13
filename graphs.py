import plotly.express as px


def create_histogram(dataframe, dep, fuel, target):
    # Ensuring that filters exist by setting default values
    if fuel is None:
        fuel = 'E10'
    if dep is None:
        dep = 94

    # Getting filtered data matching parameters
    data = dataframe.query("prix_nom == '" + fuel + "' and dep_code == '" + str(dep) + "'")[target]
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
