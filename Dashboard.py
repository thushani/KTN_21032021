import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash import Input, Output
import pandas as pd
from jproperties import Properties



app = dash.Dash(__name__)

configs = Properties()
with open('app-config.properties', 'rb') as config_file:
    configs.load(config_file)
print(configs.get("DATA_PATH"))
df = pd.read_csv(configs.get("DATA_PATH").data)
df['Date'] = pd.to_datetime(df['Date'])
df = df[(df['Date'] > '2008-01-01') & (df['Date'] <= '2008-12-31')]
fig = px.scatter(df, x='Date', y='Adj Close', trendline="ewm", trendline_options=dict(halflife=2))

app.layout = html.Div([
    html.Div([html.H1("Moving Average For Apple Stocks ")], style={'textAlign': "center"}),
    html.Div([
        html.Div([
            html.Div([dcc.Graph(figure=fig)], className="row", style={"margin": "auto"}),
            html.Div([html.Button("Download Excel", id="btn_xlsx", style={'font-size': '20px',
                                                                          "background-color": "white",
                                                                          "color": "black",
                                                                          'display': 'inline-block'}),
                      dcc.Download(id="download-dataframe-xlsx")],
                     )
        ], className="row")
    ], className="six columns", style={"margin-right": 0, "padding": 0}),
], className="container")


@app.callback(
    Output("download-dataframe-xlsx", "data"),
    Input("btn_xlsx", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    return dcc.send_data_frame(df.to_excel, "AAPL.xlsx", sheet_name="AAPL_data")


if __name__ == '__main__':
    app.run(host=configs.get("HOST").data, port=configs.get("PORT").data)
