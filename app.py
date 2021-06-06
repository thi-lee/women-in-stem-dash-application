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
data.Major = data.Major.str.capitalize()

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
server = app.server
app.title = "STEM majors population stats"

app.layout = dbc.Container(
    [dbc.Row(
        [dbc.Col(
            [dbc.Card(
                [dbc.CardBody(
                    [html.H1("Number of students in STEM"),
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
            dbc.Card(
                [dbc.CardHeader("MAJOR CATEGORY", className="font-weight-bolder text-center text-info"),
                dbc.CardBody(
                    dcc.Dropdown(
                        id="major-cat-dropdown",
                        options=[
                            {'label': major_category, 'value': major_category}
                            for major_category in np.sort(data.Major_category.unique())
                        ],
                        value="Engineering"
                    ),
                    className="pt-2 pb-3 font-weight-bolder text-center"
                )]
            ),
            width=6
        ),
        dbc.Col(
            dbc.Card(
                [dbc.CardHeader("TOTAL", className="text-info text-center"),
                dbc.CardBody(id="major-cat-total")]
            ),
            width=2,
            className="major-cat-stats font-weight-bolder text-center"
        ),
        dbc.Col(
            dbc.Card(
                [dbc.CardHeader("WOMEN", className="text-info text-center"),
                dbc.CardBody(id="major-cat-women")]
            ),
            width=2,
            className="major-cat-stats font-weight-bolder text-center"
        ),
        dbc.Col(
            dbc.Card(
                [dbc.CardHeader("MEN", className="text-info text-center"),
                dbc.CardBody(id="major-cat-men")]
            ),
            width=2,
            className="major-cat-stats font-weight-bolder text-center"
        )]
    ),

    dbc.Row(
        [dbc.Col(children=[
            dbc.Card(className="pt-3", children=[
                dbc.Container(children=[
                    html.H5("Sort by major/major category"),
                    dcc.RadioItems(
                        id="pick-category",
                        inputClassName="ml-3",
                        value="Major",
                        options=[
                            {"label": "Major", "value": "Major"},
                            {"label": "Major category", "value": "Major_category"}
                        ]
                    ),
                ]),
                dbc.Container(children=[
                    html.H5("Sort by gender or all"),
                    dcc.RadioItems(
                        id="pick-gender",
                        inputClassName="ml-3",
                        value="total",
                        options=[
                            {"label": "Total", "value": "total"},
                            {"label": "Women", "value": "Women"},
                            {"label": "Men", "value": "Men"}
                        ]
                    )
                ]),
                dbc.Container(children=[
                    html.H5("Filter popularity"),
                    dcc.RadioItems(
                        id="pick-least-most",
                        inputClassName="ml-3",
                        value="category ascending",
                        options=[
                            {"label": "Default", "value": "category ascending"},
                            {"label": "Least popular to most", "value": "total ascending"},
                            {"label": "Most popular to least", "value": "total descending"}
                        ]
                    )
                ]),
                dcc.Graph(id="bar-chart")
            ])
        ]),],
        className="mt-2 mb-2"
    )],
    fluid=True
)

@app.callback(
    [Output("major-cat-total", "children"),
    Output("major-cat-women", "children"),
    Output("major-cat-men", "children")],
    [Input("major-cat-dropdown", "value")]
)
def major_cat(major_cat_dropdown):
    mask = (data.Major_category == major_cat_dropdown)
    filtered_data = data.loc[mask, :]
    major_cat_total = filtered_data.Total.sum()
    major_cat_women = filtered_data.Women.sum()
    major_cat_men = filtered_data.Men.sum()
    
    return major_cat_total, major_cat_women, major_cat_men

@app.callback(
    Output("bar-chart", "figure"),
    [Input("pick-category", "value"),
    Input("pick-gender", "value"),
    Input("pick-least-most", "value")]
)
def pick_category(pick_category, pick_gender, pick_least_most):
    
    x = data[pick_category]

    if pick_gender == "total":
        fig = go.Figure(go.Bar(x=x, y=data["Women"], name="Men"))
        fig.add_trace(go.Bar(x=x, y=data["Men"], name="Women"))
    else:
        fig = go.Figure(go.Bar(x=x, y=data[pick_gender], name=pick_gender))

    fig.update_layout(barmode="stack", xaxis={"categoryorder": pick_least_most})

    bar_chart_figure = fig

    return bar_chart_figure

if __name__ == "__main__":
    app.run_server(debug=True)