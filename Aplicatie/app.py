# app.py

import pandas as pd
from dash import Dash, dcc, html

data = (
    pd.read_csv("Sleep_Efficiency.csv")
    .query("Gender == 'Female'")
    .sort_values(by="Bedtime")
)

app = Dash(__name__)
app.title = "Sleep Well!"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="💤", className="header-emoji"),
                html.H1(
                    children="Sleep Well", className="titlu-header"
                ),
                html.P(
                    children=(
                        "Afla cat și cum dormi ca sa dormi mai mult si mai bine."
                    ),
                    className="descriere-header",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        figure={
                            "data": [
                                {
                                    "x": data["Bedtime"],
                                    "y": data["Sleep duration"],
                                    "type": "lines",
                                },
                            ],
                            "layout": {
                                "title": {
                                    "text": "Ore de somn dormite",
                                    "x": 0.05,
                                },
                                "colorway": ["#004C00"],
                            },
                        },
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        figure={
                            "data": [
                                {
                                    "x": data["Bedtime"],
                                    "y": data["Sleep efficiency"],
                                    "type": "lines",
                                },
                            ],
                            "layout": {
                                "title": {
                                    "text": "Calitatea Somnului",
                                    "x": 0.05,
                                },
                                "colorway": ["#0000b2"],
                            },
                        },
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)


if __name__ == "__main__":
    app.run_server(debug=True)