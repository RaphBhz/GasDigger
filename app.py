from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px
from graphs import calcul_distance, maps, create_histogram
from components import get_filters,get_content,NAVBAR
from geopy.geocoders import Nominatim
from api import get_geo,fetch_data,verif_adress
import dash_bootstrap_components as dbc

geolocator = Nominatim(user_agent="adamfrance@gmail.com")   
CODE_DEP = '94'
DATA_TARGET = 'prix_valeur'
df = fetch_data()
fuels = pd.unique(df['prix_nom'])
deps = pd.unique(df['dep_code'])

# Function to fetch api data

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_stylesheets = ['https://cdn.jsdelivr.net/npm/remixicon@2.5.0/fonts/remixicon.css',dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP]

app = Dash(__name__, serve_locally=True, external_stylesheets=external_stylesheets)

app.layout = html.Div(className="page", 
                    children=[
                        NAVBAR,get_filters(fuels, deps),
                        get_content()
])

###### HISTOGRAMME UPDATE #######

@app.callback(
    Output('histo-part', 'children'),
    Input('fuel-dropdown', 'value'),
    Input('dep-dropdown', 'value'),
)
def update_graph(fuel, dep):
        print("Histogramme : \n- {0}\n- {1}\n".format(fuel,dep))
        if fuel is None:
            fuel = 'E10'
        if dep is None:
            dep = '94'
        FIG = create_histogram(df, dep, fuel, DATA_TARGET)
        text = "Départment : "+ dep
        return dcc.Graph(
                figure=FIG)

###### MAP UPDATE #######
@app.callback(
    Output('map-part', 'children'),
    Input('map_button', 'n_clicks'),
    State('fuel-dropdown', 'value'),
    State('input_prix', 'value'),
    State('input_adress', 'value'),
    State('input_rayon', 'value'),
    State('input_services', 'value'))

def update_map(n_clicks, fuel, price,adress,rayon,services):
    map = html.Iframe(className="map-class", 
                       srcDoc = open('maps.html', 'r').read())
    if n_clicks > 0:
        if adress and fuel:
            position = get_geo(adress)
            print("Heyyy")
            maps(df, fuel, price[0], price[1], position, services, rayon)
        print("You have selected \n- {0}\n- {1}\n- {2}\n- {3}\n- {4}\n".format(fuel,price,adress,rayon,services))
    return map

@app.callback(
    Output('alert-carburant', 'is_open'),
    Output('alert-adresse', 'is_open'),
    Output('input_adress', 'invalid'),
    Input('fuel-dropdown', 'value'),
    Input('input_adress', 'value'))

def update_alerts(fuel,adress):
    alert_fuel= False
    alert_adress=False
    invalid_adress=False
    if adress and fuel:
        print()
    elif adress:
        alert_fuel=True
        alert_adress=False
        invalid_adress=False
    elif fuel:
        alert_fuel=False
        alert_adress=True
        invalid_adress=True
    else:
        alert_fuel=True
        alert_adress=True
        invalid_adress=True
    return alert_fuel,alert_adress,invalid_adress
if __name__ == '__main__':
    app.run_server(debug=True)