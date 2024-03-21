# app.py

import pandas as pd
from dash import Dash, dcc, html

data = (
    pd.read_csv("Sleep_Efficiency.csv")
    .query("Gender == 'Female'")
    .sort_values(by="Bedtime")
)

app = Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1(children="Sleep Well"),
        html.P(
            children=(
                "O aplicatie pentru monitorizarea somnului."
            ),
        ),
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": data["Bedtime"],
                        "y": data["Sleep duration"],
                        "type": "lines",
                    },
                ],
                "layout": {"title": "Somnul femeilor"},
            },
        ),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)