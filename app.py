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
# sorted_data = data.query("Major_category == 'Engineering'")
data.sort_values(by=['Total'], inplace=True)

# print(data.loc[data.Major == 'Biology'])

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]

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
                            {"label": "Women", "value": "women"},
                            {"label": "Men", "value": "men"}
                        ]
                    )
                ]),
                dbc.Container(children=[
                    html.H5("Filter popularity"),
                    dcc.RadioItems(
                        id="pick-least-most",
                        inputClassName="ml-3",
                        options=[
                            {"label": "Least popular to most", "value": "least_most"},
                            {"label": "Most popular to least", "value": "most_least"}
                        ]
                    )
                ]),
                dcc.Graph(id="bar-chart")
            ])
        ]),
        # dbc.Col(
        #     [dbc.Card(
        #         [html.H5("What is the difference in number of men and women in STEM by major/major_category?"),
        #         dcc.RadioItems(
        #             id="major-or-major-category",
        #             options=[
        #                 {'label': 'Major', 'value': 'Major'},
        #                 {'label': 'Major category', 'value': 'Major_category'},
        #             ],
        #             value='Major'
        #         ),
        #         dcc.Dropdown(id="pick-major", className="mb-2"),
        #         dcc.Graph(id="total_bar")],
        #         className="p-2"
        #     )],
        #     width=6
        # ),
        # dbc.Col(
        #     [dbc.Card(
        #         [html.H5("What is the most and least popular major in each major category?"),
        #         dcc.Graph(
        #             id="",
        #             figure={
        #                 "data": [
        #                     {"x": data["Major"],
        #                     "y": data["Total"],
        #                     "type": "bar"}
        #                 ],
        #                 "layout": {
                            
        #                 }
        #             },
        #             className="pb-5"
        #         )],
        #         className="p-2"
        #     )],
        #     width=6
        # )
        ],
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
    Input("pick-gender", "value")]
)
def pick_category(pick_category, pick_gender):
    
    x = data[pick_category]

    if pick_gender == "men":
        fig = go.Figure(go.Bar(x=x, y=data["Men"], name="Men"))
    elif pick_gender == "women":
        fig = go.Figure(go.Bar(x=x, y=data["Women"], name="Women"))
    elif pick_gender == "total":
        fig = go.Figure(go.Bar(x=x, y=data["Men"], name="Men"))
        fig.add_trace(go.Bar(x=x, y=data["Women"], name="Women"))
        fig.update_layout(barmode="stack", xaxis={"categoryorder": "category ascending"})

    bar_chart_figure = fig

    return bar_chart_figure

# @app.callback(
#     [Output("pick-major", "options"),
#     Output("pick-major", "value")],
#     [Input("major-or-major-category", "value")]
# )
# def choose_category(pick_category):
#     filtered_data = data[pick_category]
#     major_or_major_category = [
#         {'label': pick_category, 'value': pick_category}
#         for pick_category in np.sort(filtered_data.unique())
#     ]
#     if pick_category == 'Major_category':
#         default_value = 'Engineering'
#     else:
#         default_value = 'Computer engineering'
#     return major_or_major_category, default_value

# @app.callback(
#     Output("total_bar", "figure"),
#     [Input("pick-major", "value"),
#     Input("major-or-major-category", "value")]
# )
# def update_bar_chart(major, category):
#     if category == "Major_category":
#         mask = (
#             (data.Major_category == major)
#         )
#     elif category == "Major":
#         mask = (
#             (data.Major == major)
#         )

#     filtered_data = data.loc[mask, :]

#     x = filtered_data[category]
#     fig = go.Figure(go.Bar(x=x, y=filtered_data["Men"], name="Men", marker_color="#1F3F49"))
#     fig.add_trace(go.Bar(x=x, y=filtered_data["Women"], name='Women', marker_color="#CED2CC"))
#     fig.update_layout(barmode='stack', xaxis={'categoryorder':'category ascending'})

#     total_bar_figure = fig
#     return total_bar_figure

if __name__ == "__main__":
    app.run_server(debug=True)