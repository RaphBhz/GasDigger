# Python libraries
import dash
from dash import dcc, Input, Output
from dash import html

# Project utility
from graphs import create_histogram
from api import fetch_data
from components import NAVBAR, get_content, get_filters


# Creates or updates the dash app layout
def create_layout(dash_app, fuels=None, deps=None, figure=None):
    if deps is None:
        deps = []
    if fuels is None:
        fuels = []

    dash_app.layout = \
        html.Div(id="page", children=[
            NAVBAR,
            html.Div(id="mainframe",
                     children=[
                         get_filters(fuels, deps),
                         get_content(figure)
                     ]),
            dcc.Interval(id='init-interval', interval=100000, n_intervals=0, disabled=False)
        ])


if __name__ == '__main__':
    # Creating dataframe variable that will be used to store data
    # We create this variable here, so we can implement a loader while we fetch the api
    df = None

    # Creating the Dash app
    app = dash.Dash(__name__)
    create_layout(app)

    # Implementing interactivity
    @app.callback(
        [Output(component_id='mainframe', component_property='children'),
         Output(component_id='init-interval', component_property='disabled')],
        [Input(component_id='init-interval', component_property='n_intervals'),
         Input(component_id='mainframe', component_property='children')]
    )
    # Initializing the mainframe, this function allows to implement a loader while waiting for the data
    def init_mainframe(n, mainframe):
        global df
        if df is not None:
            return mainframe, True
        # Fetching data from api
        data = fetch_data()
        df = data['data']
        fuels = data['fuels']
        deps = data['deps']
        # Preparing graph to display
        figure = create_histogram(df, 'E10', '94', 'prix_valeur')
        return [[get_filters(fuels, deps), get_content(figure)], True]

    @app.callback(
        # Changing fuel type or department
        Output(component_id='graph-fuel', component_property='figure'),
        [Input(component_id='fuel-dropdown', component_property='value'),
         Input(component_id='dep-dropdown', component_property='value'),
         Input(component_id='init-interval', component_property='disabled')],
    )
    def update_figure(fuel_value, dep_value, _):
        global df
        return create_histogram(df, fuel_value, dep_value, 'prix_valeur')


    # Run the Dash app
    app.run(debug=True)
