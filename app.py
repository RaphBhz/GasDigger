import pandas as pd
import dash
from dash import dcc, Input, Output
from dash import html

from graphs import create_histogram

# Setting the context
CSV_PATH = './data/fuel_data.csv'
CODE_DEP = '94'
DATA_TARGET = 'prix_valeur'
df = pd.read_csv(CSV_PATH, delimiter=';')
fuels = pd.unique(df['prix_nom'])
deps = pd.unique(df['dep_code'])
deps = deps.astype('str')
deps.sort()

if __name__ == '__main__':
    # Preparing graph to display
    figure = create_histogram(df, CODE_DEP, fuels[0], DATA_TARGET)

    # Creating the Dash app
    app = dash.Dash(__name__)
    app.layout = html.Div(children=[
        html.Div(children=[
            html.H2('Carburant'),
            dcc.Dropdown(
                id='fuel-dropdown',
                options=fuels,
                searchable=False,
                placeholder='Selectionnez un carburant',
                style={'width': '40%'}
            ),
            html.H2('Département'),
            dcc.Dropdown(
                id='dep-dropdown',
                options=deps,
                searchable=True,
                placeholder='Selectionnez un département',
                style={'width': '40%'}
            )],
            style={'display': 'flex', 'flex-direction': 'line', 'flex-align': 'center',
                   'align-items': 'center', 'justify-content': 'center', 'width': '100%'}
        ),
        html.H1(children=f'', id='page-title'),
        dcc.Graph(
            id='graph-fuel',
            figure=figure
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
