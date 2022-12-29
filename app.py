from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px
from graphs import calcul_distance, maps, create_histogram
from components import get_filters,get_content,NAVBAR
from geopy.geocoders import Nominatim
from api import get_geo,fetch_data

CODE_DEP = '94'
DATA_TARGET = 'prix_valeur'
df = fetch_data()
fuels = pd.unique(df['prix_nom'])
deps = pd.unique(df['dep_code'])

# Function to fetch api data

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, serve_locally=True, external_stylesheets=external_stylesheets)

app.layout = html.Div(className="page", 
                    children=[
                        NAVBAR,get_filters(fuels, deps),
                        get_content()
])


@app.callback(
    Output('graph-fuel', 'children'),
    Input('histogramme_button', 'n_clicks'),
    State('fuel-dropdown', 'value'),
    State('dep-dropdown', 'value'),
)
def update_graph(n_clicks, fuel, dep):
    if n_clicks > 0:
        print("Histogramme : \n- {0}\n- {1}\n".format(fuel,dep))
        if fuel is None:
            fuel = 'E10'
        if dep is None:
            dep = '94'
        FIG = create_histogram(df, dep, fuel, DATA_TARGET)
        text = "Départment : "+ dep
        return html.H3(text),dcc.Graph(
                figure=FIG)


@app.callback(
    Output('map', 'children'),
    Input('map_button', 'n_clicks'),
    State('fuel-dropdown', 'value'),
    State('input_prix', 'value'),
    State('input_adress', 'value'),
    State('input_rayon', 'value'),
    State('input_services', 'value'))

def update_map(n_clicks, fuel, price,adress,rayon,services):
    if n_clicks > 0:
        if adress:
            position = get_geo(adress)
            maps(df, fuel, price[0], price[1], position, services, rayon)
        print("You have selected \n- {0}\n- {1}\n- {2}\n- {3}\n- {4}\n".format(fuel,price,adress,rayon,services))
    return html.Iframe(id = 'map-part', 
                       srcDoc = open('maps.html', 'r').read(),
                       style={"width": "100%"},
                       height = '400')

if __name__ == '__main__':
    app.run_server(debug=True)