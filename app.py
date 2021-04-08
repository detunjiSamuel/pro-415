#!/usr/bin/env python3
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input

import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

data = pd.read_csv("obesity-cleaned.csv")
data['Obesity'] = data['Obesity'].str.extract(pat = '(\d*.\d*)',expand=True)

#data["Date"] = pd.to_datetime(data["Date"], format="%Y-%m-%d")
data.sort_values("Year", inplace=True)




external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = "Obesity Analytics"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(
                    children="OBESITY ANALYTICSS", className="header-title"
                ),
                html.P(
                    children="ANALYSE OBESITY "
                    "AMONG ADULTS BY COUNTRY"
                    " between 1975 and 2016",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Country", className="menu-title"),
                        dcc.Dropdown(
                            id="country-filter",
                            options=[
                                {"label": country, "value": country}
                                for country in np.sort(data.Country.unique())
                            ],
                            value="Afghanistan",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Sex", className="menu-title"),
                        dcc.Dropdown(
                            id="sex-filter",
                            options=[
                                {"label": sex, "value": sex}
                                for sex in data.Sex.unique()
                            ],
                            value="Both sexes",
                            clearable=False,
                            searchable=False,
                            className="dropdown",
                        ),
                    ],
                ),
                html.Div(
                    children=[
                        html.Div(
                            children="Year Range", className="menu-title"
                        ),
                        dcc.Dropdown(
                            id="year-filter",
                            options=[
                                {"label": year, "value": year}
                                for year in data.Year.unique()
                            ],
                            value="2016",
                            clearable=False,
                            searchable=False,
                            className="dropdown",
                        ),
                    ]
                ),
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="year-chart",
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="sex-chart",
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)
"""         & (data.Country == country )
        & (data.Obesity == obesity)
 """

@app.callback(
    [Output("year-chart", "figure"), Output("sex-chart", "figure")],
    [
        Input("country-filter", "value"),
        Input("sex-filter", "value"),
        Input("year-filter", "value"),
    ],
)
def update_charts(country ,sex, year):
    mask = (
        (data.Year == year)
        & (data.Sex == sex)
        #& (data.Obesity == obesity)

    )
    filtered_data = data.loc[mask, :]

    #i think i should put the year year and obesity in an array
    sam_filter = (
        (data.Country == country)
        & (data.Sex == 'Male')
    )
    filtered = data.loc[sam_filter,:]

    sa_filter = (
        (data.Country == country)
        & (data.Sex == 'Female')
    )
    filtere = data.loc[sa_filter,:]  

    print(filtered["Obesity"])
    male_chart_figure = {
        "data": [
            {
                "x": filtered["Year"],
                "y": filtered["Obesity"],
                "type": "lines",
                "hovertemplate": "%{y:.2f}(%)<extra></extra>",
                'name': 'Male',
                'color': 'darkgrey'
            },
            {
                "x": filtere["Year"],
                "y": filtere["Obesity"],
                'name': 'Female',
                "type": "lines",
            },

        ],
        "layout": {
            "title": {
                "text": "Average obesity in Males and Females over the years in %s "%country,
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "%", "fixedrange": True},
            #"colorway": ["#17B897"],
        },
    }

    sam_filter = (
        (data.Country == country)
        & (data.Sex == 'Both sexes')
    )
    filtered = data.loc[sam_filter,:]
    new_list = [x+30 for x in filtered["Year"]]
    
    female_chart_figure = {
        "data": [
            {
                "x": new_list,
                "y": filtered["Obesity"],
                'name':'train',
                'mode':'markers',
                "type": "scatter",
            },
        ],
        "layout": {
            "title": {"text": "Predicted obesity for future years in %s "%country, "x": 0.05, "xanchor": "left"},
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "%", "fixedrange": True},
            "colorway": ["#E12D39"],
        },
    }
    return male_chart_figure, female_chart_figure




if __name__ == "__main__":
    app.run_server(debug=True)
