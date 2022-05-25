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
        dcc.Graph(id='trend-graph'),
            html.Div([


                html.Div([
                    'TOP',
                    dcc.Slider(1, 15, 1,
                               # marks=None,
                               value=5,
                               id='input-th'),
                ],
                    style={'width': '500px',
                           # 'display': 'inline-block',
                           'padding': '0px',
                           'margin': '0 auto'
                           }
                ),

                html.Div([
                    'Year  ',
                    dcc.Input(id='input-year', value='', type='text')
                ],
                    style={'width': '500px',
                           # 'display': 'inline-block',
                           'padding': '0px',
                           'margin': '0 auto',
                           'position': 'absolute',
                           'left': '310px',
                           }
                ),

                html.Div(
                    id='the-alert',
                    children=[],
                    style={'display': 'inline-block',
                           'position': 'absolute',
                           'height': '50px',
                           'left': '500px'
                           }
                ),

                html.Div([
                    dcc.RadioItems(
                        id='input-sex',
                        options=[
                            {'label': 'Female', 'value': 'F'},
                            {'label': 'Male', 'value': 'M'},
                        ],
                        value='M'
                    )
                ],
                style={'width': '150px',
                      # 'display': 'inline-block',
                      'margin': '0 auto',
                      'position': 'absolute',
                      'top':'90px',
                      'left': '500px',
                }),

            ],
            style={
                'margin':'0 auto',
                'position':'relative'
            })
    ]),
],

)

alert = dbc.Alert("Please input year between 1910-2020", color='danger', dismissable=False, duration=100000)

@app.callback(
    Output('trend-graph', 'figure'),
    Output('the-alert', 'children'),
    Input('input-year', 'value'),
    Input('input-sex', 'value'),
    Input('input-th', 'value')
)

def update_figure(year, sex, th):
    if year not in df.year.values and year != '':
        return [], alert
    year = int(year)
    th = int(th)

    names = df.groupby(['name', 'year', 'sex'])['count'].sum().reset_index()
    sort_names = names.sort_values(by=['year', 'count'], ascending=False)
    sort_names_year = sort_names[sort_names['year'] == year]
    sort_names_year_sex = sort_names_year[sort_names_year['sex'] == sex]
    sort_names_year_sex_th = sort_names_year_sex.head(th)
    c = [i for i in range(th)]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=sort_names_year_sex_th['count']
                         , y=sort_names_year_sex_th['name']
                         , orientation='h'
                         , marker=dict(color=c, colorscale='RdBu')))
    fig.update_layout(uniformtext_minsize=2, uniformtext_mode='hide', showlegend=False
                      , yaxis={'categoryorder': 'total ascending'}
                      , plot_bgcolor='rgba(0,128,0,0.3)'
                      , title_text="Top " + str(th) + " Popular Names in " + str(year))
    return fig, dash.no_update


if __name__ == '__main__':
    app.run_server()



