import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import plotly.graph_objects as go
import plotly.express as px
import dash
from dash import Dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

app = Dash(__name__)

df = pd.read_csv(r'baby-names-state.csv')

app.layout = html.Div([
    html.Div([
        html.H6("Trend of Name"),

    ]),
    dcc.Graph(id='trend-graph'),
    html.Div([
        html.Div([
            "Name: ",
            dcc.Input(id='input-name', value='', type='text')
        ],
            style={'height':'50px',
                   'display':'inline-block',
                   'position': 'absolute',
                   'left': '120px'
                   }
        ),
        html.Div(
            id='the-alert',
            children=[],
            style={'display':'inline-block',
                   'position':'absolute',
                   'height':'50px',
                   'left':'380px'
                   }
        ),
    ],
    style={
    'width':'500px',
    'height':'30px',
    'margin': '0 auto',
    'position':'relative'
    }),


    html.Div([
        dcc.RadioItems(
            id='input-sex',
            options=[
                {'label': 'Female', 'value': 'F'},
                {'label': 'Male', 'value': 'M'},
            ],
            value='M',
        )
    ],
    style={'width': '160px',
           # 'display': 'inline-block',
           'padding': '0px',
           'margin': '10px auto'
           }
    ),
])

alert = dbc.Alert("Invalid Name!", color="danger", dismissable=False, duration=1500)

@app.callback(
    Output('trend-graph', 'figure'),
    Output('the-alert', 'children'),
    Input('input-name', 'value'),
    Input('input-sex', 'value'))
def update_figure(name, sex):
    if name not in df.name.values and name != '':  # if illegal, make graph blank and show alert
        return [], alert
    name_df = df.loc[df['name'] == name].reset_index(drop=True)
    sex_name_df = name_df.loc[name_df['sex'] == sex]
    sex_df = df.loc[df['sex'] == sex].groupby(['year', 'name']).sum()

    all_years = df['year'].unique()
    years_used = []
    rank_list = []
    for year in all_years:
        year_f = sex_df.loc[year].sort_values("count", ascending=False)['count']
        try:
            years_used.append(year)
            rank = (np.where(year_f.index == name)[0] + 1) / len(year_f)
            if len(rank) == 0:
                rank_list.append(0)
            else:
                rank_list.append(1 - rank[0])
        except:
            pass

    fig = go.Figure()
    year_sex_name_df = sex_name_df.groupby('year').sum()
    fig.add_trace(go.Scatter(x=year_sex_name_df.index, y=year_sex_name_df['count'], name='Total Number'))
    fig.add_trace(go.Bar(x=years_used, y=rank_list, name='Popularity'))
    fig.update_layout(title={'text': f"Trend of " + name + " Over Time", 'x': 0.5,
                             'xanchor': 'center', 'font': {'size': 20}}, xaxis_title="Year",
                      yaxis_title="Value (log scale)")
    fig.update_yaxes(type="log")

    return fig, dash.no_update


if __name__ == '__main__':
    app.run_server()