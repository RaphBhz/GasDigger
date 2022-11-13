# Python libraries
import pandas as pd
import dash
from dash import dcc, Input, Output
from dash import html

# Project utility
from graphs import create_histogram
from api import fetch_data
from components import NAVBAR, get_content, get_filters

# Setting the context
CODE_DEP = '94'
DATA_TARGET = 'prix_valeur'
df = fetch_data()
fuels = pd.unique(df['prix_nom'])
deps = pd.unique(df['dep_code'])
deps = deps.astype('str')
deps.sort()

if __name__ == '__main__':
    # Preparing graph to display
    figure = create_histogram(df, CODE_DEP, fuels[0], DATA_TARGET)

    # Creating the Dash app
    app = dash.Dash(__name__)
    app.layout = html.Div(className="page", children=[
                                            NAVBAR,
                                            html.Div(className="mainframe",
                                                   children=[
                                                       get_filters(fuels, deps),
                                                       get_content(figure)
                                                   ]
                                            )
    ])

    # Implementing interactivity
    @app.callback(
    # Changing fuel type
    Output(component_id='graph-fuel', component_property='figure'),
    [Input(component_id='fuel-dropdown', component_property='value'),
    Input(component_id='dep-dropdown', component_property='value')]
    )
    def update_figure(fuel_value, dep_value):
        return create_histogram(df, dep_value, fuel_value, DATA_TARGET)


    # Run the Dash app
    app.run_server(debug=True)
