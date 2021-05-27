import dash
import dash_core_components as dcc 
import dash_html_components as html 
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
from dash.dependencies import Input, Output
import plotly.graph_objects as go

data = pd.read_csv("women-stem.csv")
# data = data.query("Major_category == 'Engineering'")
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])
app.title = "Women in STEM"

app.layout = dbc.Container(
    [dbc.Row(
        [dbc.Col(
            [dbc.Card(
                [dbc.CardBody(
                    [html.H1("Women in STEM"),
                    html.P("Let's see how it goes")]
                )]
            )],
            width=12
        )],
        className="mt-2 mb-2"
    ),

    dbc.Row(
        [dbc.Col(
            [dbc.Card(
                [dcc.Dropdown(
                    id="pick-major",
                    options=[
                        {'label': major_category, 'value': major_category}
                        for major_category in np.sort(data.Major_category.unique())
                    ],
                    value="Engineering",
                    className="mb-2"
                ),
                dcc.Graph(id="total_bar")]
            )]
        )],
        className="mt-2 mb-2"
    )],
    fluid=True
)

@app.callback(
    Output("total_bar", "figure"),
    [Input("pick-major", "value")]
)
def update_bar_chart(Major_category):
    mask = (
        (data.Major_category == Major_category)
    )
    filtered_data = data.loc[mask, :]

    x = filtered_data["Major_category"]
    fig = go.Figure(go.Bar(x=x, y=filtered_data["Men"], name="Men", marker_color="#1F3F49"))
    fig.add_trace(go.Bar(x=x, y=filtered_data["Women"], name='Women', marker_color="#CED2CC"))
    fig.update_layout(barmode='stack', xaxis={'categoryorder':'category ascending'})

    total_bar_figure = fig
    return total_bar_figure

if __name__ == "__main__":
    app.run_server(debug=True)