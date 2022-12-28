from dash import dcc, Input, Output
from dash import html

NAVBAR = html.Div(id="navbar", children=[html.H1("GasDigger")])


def get_content(figure):
    if figure is None:
        return html.Div(id='content', style={"width": "100%", "height": "100%"}, children=[
            html.H1("Chargement...", id='graph-title', style={"font-family": "'Josefin Sans', sans-serif", "padding-left": "10px"}),
            html.Img(src='./assets/media/loading.gif'),
            dcc.Graph(id='graph-fuel', figure={}, style={"display": "None"})
        ])

    return html.Div(id='content', style={"width": "100%", "height": "100%"}, children=[
        html.H1("Graph", id='graph-title', style={"font-family": "'Josefin Sans', sans-serif", "padding-left": "10px"}),
        dcc.Graph(id='graph-fuel', figure=figure)
    ])


def get_filters(fuels, deps):
    return html.Div(id="filters",
                    children=[
                        html.Div(className="filter",
                                 children=[
                                     html.H2('Carburant'),
                                     dcc.Dropdown(
                                         id='fuel-dropdown',
                                         options=fuels,
                                         searchable=False,
                                         placeholder='Carburant',
                                     )
                                 ]),
                        html.Div(className="filter",
                                 children=[
                                     html.H2('Département'),
                                     dcc.Dropdown(
                                         id='dep-dropdown',
                                         options=deps,
                                         searchable=True,
                                         placeholder='Département',
                                     )
                                 ])
                    ])
