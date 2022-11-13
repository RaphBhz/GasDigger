import dash
from dash import dcc, Input, Output
from dash import html

NAVBAR = html.Div(className="navbar", children=[html.H1("GasDigger")])

def get_content(figure):
    return html.Div(children=
            [html.H1("Graph", id='graph-title'),
            dcc.Graph(
               id='graph-fuel',
               figure=figure,
               style={"width": "100%", "height": "100%"}
            )])

def get_filters(fuels, deps):
    return html.Div(className="filters",
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