# app.py

import pandas as pd
from dash import Dash, Input, Output, dcc, html

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
                    children="Sleep Wel", className="titlu-header"
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
                    children=[
                        html.Div(
                            children="Interval Calendaristic", className="titlu-menu"
                        ),
                        dcc.DatePickerRange(
                            id="interval-date",
                            min_date_allowed=pd.to_datetime(data["Bedtime"]).min().date(),
                            max_date_allowed=pd.to_datetime(data["Bedtime"]).max().date(),
                            start_date=pd.to_datetime(data["Bedtime"]).min().date(),
                            end_date=pd.to_datetime(data["Bedtime"]).max().date(),
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
                        id="ore-dormite",
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="calitate-somn",
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)

@app.callback(
    Output("ore-dormite", "figure"),
    Output("calitate-somn", "figure"),
    Input("interval-date", "start_date"),
    Input("interval-date", "end_date"),
)
def update_charts(start_date, end_date):
    filtered_data = data.query(
        "Bedtime >= @start_date and Bedtime <= @end_date"
    )
    figura_grafic_ore_dormite = {
        "data": [
            {
                "x": filtered_data["Bedtime"],
                "y": filtered_data["Sleep duration"],
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
    }

    figura_grafic_calitate_somn = {
        "data": [
            {
                "x": filtered_data["Bedtime"],
                "y": filtered_data["Sleep efficiency"],
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
    }
    return figura_grafic_ore_dormite, figura_grafic_calitate_somn

if __name__ == "__main__":
    app.run_server(debug=True)