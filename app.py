import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html


# Setting the context
CSV_PATH='./data/fuel_data.csv'
CODE_DEP='94'
FUEL='E10'
DATA_TARGET='prix_valeur'

# Getting data from the
df = pd.read_csv(CSV_PATH, delimiter=';')
data = df.query("prix_nom == '" + FUEL + "' and dep_code == '" + CODE_DEP + "'")[DATA_TARGET]
print(data.describe())

# Preparing the graph
figure = px.histogram(data, x=DATA_TARGET)

# Creating the Dash app
if __name__ == '__main__':

    app = dash.Dash(__name__):
    app.layout = html.Div(children=[

        html.H1(
            children=f'Reparition of {FUEL} cost in gas stations in departement {CODE_DEP} of France.',
            style={'textAlign': 'center', 'color': '#FF0000'}
        ),

        dcc.Graph(
            id=FUEL + '_' + CODE_DEP,
            figure = figure
        )
    ])


    # Run the Dash app
    app.run_server(debug=True)
