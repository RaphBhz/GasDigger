from dash import Dash, dcc, html
import dash_bootstrap_components as dbc

PLOTLY_LOGO = "/assets/logo.png"

alert_carburant = dbc.Alert(
                "Veuillez-choisir un carburant",
                id="alert-carburant",
                is_open=False,
                dismissable=True,
                color="danger",
        )
alert_adresse =  dbc.Alert(
                "Adresse postale incorrect",
                id="alert-adresse",
                is_open=False,
                dismissable=True,
                color="danger",
        )

NAVBAR = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                        dbc.Col(dbc.NavbarBrand("Gas Digger", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                #href="https://plotly.com",
                style={"textDecoration": "none"},
            )
        ]
    ),
    color="dark",
    dark=True,
)

def get_content():
    histogramme = dbc.Card(
    dbc.CardBody(
        [
            html.Div(id="histo-part",className ="graphs", children=[
            ])
        ]
    ),
    className="mt-3",
    )
    map = dbc.Card(
    dbc.CardBody(
        [
            html.Div(id="map-part",className ="graphs",children=[
            ])
        ]
    ),
    className="mt-3",
    )
    return dbc.Tabs([
        dbc.Tab(histogramme,label='Histogramme',tab_id='graph-fuel'),
        dbc.Tab(map,label='Map', tab_id='map')
    ],className="tabs")

def get_filters(fuels, deps):
    list_services = ['Toilettes publiques',
        'Boutique',
        'Station de gonflage',
        'Automate CB 24/24','Wifi','Restauration']
    return html.Div(className="filters",
                    children=[
                        dbc.Row(
                                [
                                dbc.Col(html.Div(className="fuel-filter",
                                    children=[
                                        html.I(className="ri-oil-line icon-filter"),
                                        dcc.Dropdown(
                                        id='fuel-dropdown',
                                        options=fuels,
                                        searchable=False,
                                        placeholder='Carburant',
                                        className="dropdown right-filter"
                                )])),
                                dbc.Col(html.Div(className="dep-filter",
                                    children=[
                                        html.I(className="ri-numbers-line icon-filter"),
                                        html.Div(className="fblock float-right", children=[dcc.Dropdown(
                                            id='dep-dropdown',
                                            options=deps,
                                            searchable=True,
                                            placeholder='Département',
                                            className="dropdown right-filter"
                                        )])
                                    ])),
                            ]),

                        html.Div(className="filter adress",
                            children=[
                            html.I(className="ri-map-pin-5-fill icon-filter"),
                            dbc.Input(
                                id="input_adress",
                                type='text',
                                value=None,
                                placeholder="Saisissez votre adresse",
                                valid=False, invalid=False, className="mb-3"
                            ),
                            html.Div(id="search-results")
                            ]),

                        html.Div(className="filter rayon",
                            children=[
                            html.A('Rayon de recherche'),
                            dcc.Slider(0, 100,
                                value=30,
                                tooltip={"placement": "bottom", "always_visible": True},
                                id='input_rayon',
                                marks={
                                    0: {'label': '0 km', 'style': {'color': '#77b0b1'}},
                                    25: {'label': '25 km'},
                                    50: {'label': '50 km'},
                                        75: {'label': '75 km'},
                                    100: {'label': '100km', 'style': {'color': '#f50'}}
                                },
                            )
                            ]),

                        html.Div(className="filter price",
                            children=[
                            html.P('Prix en € par litre'),
                            dcc.RangeSlider(
                                0, 2,
                                value=[0.8, 1.6], 
                                tooltip={"placement": "bottom", "always_visible": True},
                                id='input_prix'),   
                            ]),
                        
                        
                        html.Div(
                            [
                                dbc.Label("Services"),
                                dbc.Checklist(
                                    options=[{'label': dom, 'value': dom} for dom in list_services],
                                    id='input_services',
                                    switch=True,
                                    inline=True
                                ),
                            ]
                        ),
                        dbc.Button(
                        [
                            "DIGGER",
                        ],
                        color="primary",
                        id='map_button', 
                        n_clicks=0
                        ),
                        html.Div(className="alerts",
                            children=[alert_carburant ,alert_adresse]),
                        
                        
                    ])