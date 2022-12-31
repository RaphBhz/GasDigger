from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
from dash.long_callback import DiskcacheLongCallbackManager
import pandas as pd
import plotly.express as px
from graphs import calcul_distance, maps, create_histogram
from components import get_filters,get_content,NAVBAR
from geopy.geocoders import Nominatim
from api import get_geo,fetch_data,verif_adress
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc

## Diskcache
import diskcache,time

cache = diskcache.Cache("./cache")
long_callback_manager = DiskcacheLongCallbackManager(cache)


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
theme = {"colorScheme": "light",
        "primaryColor": "red",
        "background":"black"
    }
app.layout = dmc.MantineProvider(
    theme=theme,
    children=[
            NAVBAR,get_filters(fuels, deps),
            get_content()
    ],
    id="provider"
    )
###### HISTOGRAMME UPDATE #######

@app.callback(
    Output('histo-part', 'children'),
    Input('fuel-dropdown', 'value'),
    Input('dep-dropdown', 'value'),
    Input('provider', 'theme'),
)
def update_graph(fuel, dep, theme):
        print("Histogramme : \n- {0}\n- {1}\n".format(fuel,dep))
        if fuel is None:
            fuel = 'E10'
        if dep is None:
            dep = '94'
        FIG = create_histogram(df, dep, fuel, DATA_TARGET, theme["primaryColor"])
        return dcc.Graph(
                figure=FIG)

###### MAP UPDATE #######
@app.long_callback(
    output=Output('map-part', 'children'),
    inputs=Input('map_button', 'n_clicks'),
    state=[State('fuel-dropdown', 'value'),
    State('input_prix', 'value'),
    State('search-bar', 'value'),
    State('input_rayon', 'value'),
    State('input_services', 'value')],
    manager=long_callback_manager,
    running=[
        (Output("map_button", "disabled"), True, False),
    ],)

def update_map(n_clicks, fuel, price,position,rayon,services):
    if n_clicks > 0:
        if position and fuel:
            pos=str(position[0])+','+str(position[1])
            maps(df, fuel, price[0], price[1], pos, services, rayon)
        print("You have selected \n- {0}\n- {1}\n- {2}\n- {3}\n- {4}\n".format(fuel,price,position,rayon,services))
    return html.Iframe(className="map-class", 
                       srcDoc = open('maps.html', 'r').read())

## BARRE DE RECHERCHE

@app.long_callback(
    output=Output("search-bar", "data"),
    inputs=Input("input_adress", "value"),
    manager=long_callback_manager,
)
def callback(value):    
    if value:
        time.sleep(1.0)
        print(value)
        loc = get_geo(value)
        if loc :
            data = [{'label': l[0], 'value': l[1]} for l in loc]
            print(data)
            return data
    else:
        return []


@app.callback(
    Output('provider', 'theme'),
    Input('pick-color', 'value'),Input('provider', 'theme'),
)

def color_update(value,theme):
    print(theme)
    theme["primaryColor"]=value
    return theme

if __name__ == '__main__':
    app.run_server()#debug=True)
