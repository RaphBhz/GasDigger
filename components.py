from dash import Dash, dcc, html

NAVBAR = html.Div(className="navbar", children=[html.H1("GasDigger")])


def get_content():
    return dcc.Tabs([
        dcc.Tab(label='Histogramme',id='graph-fuel',children=[]),
        dcc.Tab(label='Map', id='map', children=[])
    ])

def get_filters(fuels, deps):
    list_services = ['Toilettes publiques',
        'Boutique',
        'Station de gonflage',
        'Automate CB 24/24']
    return html.Div(className="filters",
                    style={"width": "30%",
                    "height": "100%",
                    "float":"left",
                    },
                    children=[
                        html.Div(className="filter",
                            children=[
                            html.P('Carburant'),
                            dcc.Dropdown(
                            id='fuel-dropdown',
                            options=fuels,
                            searchable=False,
                            placeholder='Carburant'
                            )
                            ]),
                        html.Div(className="filter",
                            children=[
                            html.P('Prix'),
                            dcc.RangeSlider(
                                0.5, 2, 0.1, 
                                value=[1.5, 1.6], 
                                id='input_prix'),
                            ]),
                        
                        html.Div(className="filter",
                            children=[
                            html.P('Département'),
                            dcc.Dropdown(
                                id='dep-dropdown',
                                options=deps,
                                searchable=True,
                                placeholder='Département',
                            )
                            ]),
                        html.Div(className="filter",
                            children=[
                            html.P('Adresse'),
                            dcc.Input(
                                id="input_adress",
                                type='text',
                                placeholder="Saisissez votre adresse",
                            ),
                            html.P('Rayon'),
                            dcc.Slider(0, 100, 10,
                                value=30,
                                id='input_rayon'
                            ),
                            ]),
                        
                        html.Div(className="filter",
                            children=[
                            html.P('Services'),
                            dcc.Checklist(
                                id='input_services',
                                options=[{'label': dom, 'value': dom} for dom in list_services]
                            ),
                            ]),
                        html.P('Génerer'),
                        html.Button('HISTOGRAMME', id='histogramme_button', n_clicks=0),
                        html.Button('MAP', id='map_button', n_clicks=0)])