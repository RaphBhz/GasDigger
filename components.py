from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify
PLOTLY_LOGO = "/assets/logo.png"
COLOR = "#000000"

# fmt: off
swatches = [
    "red",
    "blue",
    "lime",
    "yellow",
    "dark"
]
# fmt: on

pick_color=dmc.ColorPicker(swatches=swatches, 
                        swatchesPerRow=7, 
                        withPicker=False,
                        id="pick-color",
                        value="red"
                    )

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
                        dbc.Col(dmc.ThemeIcon(DashIconify(icon="fa6-solid:oil-well"))),
                        dbc.Col(dbc.NavbarBrand("Gas Digger", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
            )
            , 
            pick_color

        ]
    ),
    color="black",
    dark=True,
)

selects=dmc.Select(
    nothingFound="Aucun résultat",
    icon=dmc.ThemeIcon(DashIconify(icon="radix-icons:magnifying-glass")),
    rightSection=DashIconify(icon="radix-icons:chevron-down"),
    id="search-bar",
    placeholder="Choisissez une des adresses",
)

adresse = dmc.TextInput(
                placeholder="Adresse",
                rightSection=dmc.ThemeIcon(DashIconify(icon="dashicons:admin-home"),variant="subtle",color='primary'),
                id="input_adress",
                label="Adresse",
            )

tri_adresse = html.Div(
    [
        dmc.Stack(
        children=[
            adresse,
            selects
        ],
        )

    ]
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
            dmc.LoadingOverlay(
            html.Div(id="map-part",className ="graphs"),
            loaderProps={"variant": "dots", "color": 'primary', "size": "xl"},
        )]),
    className="mt-3",
    )
    tabs = dmc.Tabs(
        [
        dmc.TabsList(
            [
                dmc.Tab("Histogramme", value="histo"),
                dmc.Tab("Carte à stations", value="carte"),
            ]
        ),
        dmc.TabsPanel(histogramme, value="histo"),
        dmc.TabsPanel(map, value="carte"),
        ],
        color='primary',
        orientation="horizontal",
        value="histo",
        
    )
    return tabs

def carburant_dropdown(fuels):
    container = html.Div(className="fuel-filter",
                                        children=[
                                    dmc.Select(
                                            label="Carburant",
                                            placeholder="Choisir un carburant",
                                            id='fuel-dropdown',
                                            data=[{'value': fuel, 'label': fuel} for fuel in fuels],                                        
                                            icon=dmc.ThemeIcon(DashIconify(icon="ri:oil-line"),variant="light"),
                                            rightSection=DashIconify(icon="radix-icons:chevron-down"),
                                            ),
                                    ])
    return container

def dep_dropdown(deps):
    container = html.Div(className="dep-filter",
                                        children=[
                                    dmc.Select(
                                            label="Département",
                                            placeholder="Choisir un département",
                                            id='dep-dropdown',
                                            data=[{'value': dep, 'label': dep} for dep in deps],
                                            icon=dmc.ThemeIcon(DashIconify(icon="ri:numbers-line"),variant="light"),
                                            rightSection=DashIconify(icon="radix-icons:chevron-down"),
                                            ),
                                    ])
    return container
            

def get_filters(fuels, deps):
    list_services = ['Toilettes publiques',
        'Boutique',
        'Station de gonflage',
        'Automate CB 24/24','Wifi','Restauration']
    print(fuels)
    return html.Div(className="filters",
                    children=[
                        dbc.Row(
                                [
                                dbc.Col(carburant_dropdown(fuels)),
                                dbc.Col(dep_dropdown(deps)),
                            ]),
                        tri_adresse,

                        html.Div(className="filter rayon",
                            children=[
                            dmc.Slider(
                                min=0, 
                                max=100,
                                value=30,
                                id='input_rayon',
                                marks=[
                                    {"value": 25, "label": "25 km"},
                                    {"value": 50, "label": "50 km"},
                                    {"value": 75, "label": "75 km"},
                                ],
                                color='primary',
                            )
                            ]),

                        html.Div(className="filter price",
                            children=[
                            html.Label('Prix en € par litre'),
                            dmc.RangeSlider(
                                value=[0.8, 1.6],
                                max=2.5,
                                min=0.3,
                                step=0.01,
                                minRange=0.1,
                                id='input_prix',
                                mb=35,
                                color='primary'
                                ),               
                                
                            ]),
                        
                        
                        html.Div(
                            [
                                dmc.CheckboxGroup(
                                    id='input_services',
                                    label="Services",
                                    #description="This is anonymous",
                                    orientation="horizontal",
                                    withAsterisk=True,
                                    offset="md",
                                    mb=10,
                                    children=[dmc.Checkbox(label=dom, value=dom, color='primary')for dom in list_services] 
                                ),
                            ]
                        ),
                        dmc.Affix(
                            dmc.Button(
                            [
                                "DIGGER",
                            ],
                            color='primary',
                            id='map_button', 
                            n_clicks=0
                            ),
                            position={"top": 340, "left": 280}
                        ),
                        
                        html.Div(className="alerts",
                            children=[alert_carburant ,alert_adresse]),
                        
                        
                    ])