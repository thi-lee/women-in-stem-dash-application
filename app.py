import dash
import dash_core_components as dcc 
import dash_html_components as html 
import dash_bootstrap_components as dbc

import plotly.express as px
from dash.dependencies import Input, Output
import plotly.graph_objects as go

import pandas as pd
import numpy as np

data = pd.read_csv("women-stem.csv")

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
server = app.server
app.title = "Women in STEM"

app.layout = dbc.Container(
    [dbc.Row(
        [dbc.Col(
            [dbc.Card(
                [dbc.CardBody(
                    [html.H1("Women in STEM"),
                    html.H3("Let's answer some questions"),
                    html.Ol([
                        html.Li("Which major is most and least popular in a major category?"),
                        html.Li("What is the difference in number of men and women in STEM by major?"),
                        html.Li("What's the total number of student in each major?"),
                    ])]
                )],
                className="p-2"
            )],
            width=12
        )],
        className="mt-2 mb-2"
    ),

    dbc.Row(
        [dbc.Col(
            [dbc.Card(
                [html.H5("What is the difference in number of men and women in STEM by major/major_category?"),
                dcc.RadioItems(
                    id="major-or-major-category",
                    options=[
                        {'label': 'Major', 'value': 'Major'},
                        {'label': 'Major category', 'value': 'Major_category'},
                    ],
                    value='Major'
                ),
                dcc.Dropdown(id="pick-major", className="mb-2"),
                dcc.Graph(id="total_bar")],
                className="p-2"
            )],
            width=6
        ),
        dbc.Col(
            [dbc.Card(
                [html.H5("What is the most and least popular major in each major category?"),
                dcc.Graph(
                    id="popularity_chart",
                    figure={
                        "data": [
                            {"x": data["Major_category"],
                            "y": data["Total"],
                            "type": "bar"}
                        ],
                        "layout": {

                        }
                    }
                )],
                className="p-2"
            )],
            width=6
        )],
        className="mt-2 mb-2"
    )],
    fluid=True
)

# in a major category (make a dropdown for this), 
# sort majors from most popular to least (total of students)
# bar chart 

@app.callback(
    [Output("pick-major", "options"),
    Output("pick-major", "value")],
    [Input("major-or-major-category", "value")]
)
def choose_category(pick_category):
    filtered_data = data[pick_category]
    major_or_major_category = [
        {'label': pick_category, 'value': pick_category}
        for pick_category in np.sort(filtered_data.unique())
    ]
    if pick_category == 'Major_category':
        default_value = 'Engineering'
    else:
        default_value = 'COMPUTER ENGINEERING'
    return major_or_major_category, default_value

@app.callback(
    Output("total_bar", "figure"),
    [Input("pick-major", "value"),
    Input("major-or-major-category", "value")]
)
def update_bar_chart(major, category):
    if category == "Major_category":
        mask = (
            (data.Major_category == major)
        )
    elif category == "Major":
        mask = (
            (data.Major == major)
        )

    filtered_data = data.loc[mask, :]

    x = filtered_data[category]
    fig = go.Figure(go.Bar(x=x, y=filtered_data["Men"], name="Men", marker_color="#1F3F49"))
    fig.add_trace(go.Bar(x=x, y=filtered_data["Women"], name='Women', marker_color="#CED2CC"))
    fig.update_layout(barmode='stack', xaxis={'categoryorder':'category ascending'})

    total_bar_figure = fig
    return total_bar_figure

if __name__ == "__main__":
    app.run_server(debug=True)