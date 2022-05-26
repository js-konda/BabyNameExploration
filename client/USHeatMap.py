import pandas as pd
import numpy as np
import os
import sys
import plotly.graph_objects as go
import plotly.express as px
import dash
from dash import Dash
import dash_html_components as html
import dash_core_components as dcc
from plotly.subplots import make_subplots
import plotly.offline as py
from plotly.offline import init_notebook_mode
#init_notebook_mode(connected=True)
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from app import app, df


layout = html.Div([
    dcc.Graph(id='us-heat-map-graph'),
    html.Div([
        html.Div([
            'Year  ',
            dcc.Input(id='us-heat-map-input-year', type='number')
        ],
            style={'width': '500px',
                   # 'display': 'inline-block',
                   'position': 'absolute',
                   'top': '60px',
                   'left': '470px',
            }
        ),

        html.Div(
            id='us-heat-map-the-alert1',
            children=[],
            style={'display': 'inline-block',
                   'position': 'absolute',
                   'height': '50px',
                   'top': '60px',
                   'left': '660px'
                   }
        ),

        html.Div([
            dcc.RadioItems(
                id='us-heat-map-input-sex',
                options=[
                    {'label': 'Female', 'value': 'F'},
                    {'label': 'Male', 'value': 'M'},
                ],
                value='M'
            )
        ],
        style={'width': '180px',
               # 'display': 'inline-block',
               'padding': '0px',
               'margin': '0 auto',
               }
        ),

        html.Div([
            'Name ',
            dcc.Input(id='us-heat-map-input-name', type='text')
        ],
        style={'width': '200px',
               # 'display': 'inline-block',
               'position':'absolute',
               'padding': '0px',
               'margin': '15px auto',
                'top': '12px',
                'left': '470px'

               }
        ),
        html.Div(
            id='us-heat-map-the-alert2',
            children=[],
            style={'display': 'inline-block',
                   'position': 'absolute',
                   'height': '50px',
                   'top': '60px',
                   'left': '660px'
                   }
        ),
    ],
    style={'position':'relative'}
    ),

])

alert1 = dbc.Alert("Please input year between 1910-2020!", color='danger', dismissable=False, duration=1500)
alert2 = dbc.Alert("Invaild Name!", color='danger', dismissable=False, duration=1500)



@app.callback(
    Output('us-heat-map-graph', 'figure'),
    Output('us-heat-map-the-alert1', 'children'),
    Output('us-heat-map-the-alert2', 'children'),
    Input('us-heat-map-input-name', 'value'),
    Input('us-heat-map-input-sex', 'value'),
    Input('us-heat-map-input-year', 'value')
)


def update_figure(name,sex, year):
    data = [dict(type='choropleth',
                     locationmode='USA-states',
                     autocolorscale=False,
                     marker=dict(
                         line=dict(color='rgb(255,255,255)', width=1)),
                     colorbar=dict(autotick=True, tickprefix='', title='Rank'),
                     reversescale=True,
                     )
                ]
    layout = dict(
            geo=dict(
            scope='usa',
            projection=dict(type='albers usa'),
            showlakes=True,
            lakecolor='rgb(255, 255, 255)'),
    )
    fig = dict(data=data, layout=layout)
    #your validation here
    if year not in df.year.values and year != None:
        return fig, alert1, dash.no_update
    elif name not in df.name.values and name != None:
        return fig, dash.no_update, alert2
    elif year == None or year == '':
        return fig, dash.no_update, dash.no_update
    # year = int(year)
    sex_df = df.loc[df['sex'] == sex]
    year_sex_df = sex_df.loc[sex_df['year'] == year].groupby(['state_abb', 'name']).sum().drop(['year'], axis=1)
    all_states = df['state_abb'].unique()
    states_used = []
    rank_list = []
    for state in all_states:
        state_f = year_sex_df.loc[state].sort_values("count", ascending=False)['count']
        try:
            states_used.append(state)
            rank = np.where(state_f.index == name)[0] + 1
            if len(rank) == 0:
                rank_list.append(len(state_f))
            else:
                rank_list.append(rank[0])
        except:
            pass
    data = [dict(type='choropleth',
                 locations=states_used,
                 z=rank_list,
                 locationmode='USA-states',
                 text=states_used,
                 autocolorscale=False,
                 marker=dict(
                     line=dict(color='rgb(255,255,255)', width=1)),
                 colorbar=dict(autotick=True, tickprefix='', title='Rank'),
                 reversescale=True,
                 )
            ]
    layout = dict(
        title=f"" + name + " Name Rank in " + str(year),
        geo=dict(
            scope='usa',
            projection=dict(type='albers usa'),
            showlakes=True,
            lakecolor='rgb(255, 255, 255)'),
    )
    fig = dict(data=data, layout=layout)
    # fig2 = py.iplot(fig, validate=False, filename='USmap')
    return fig, dash.no_update, dash.no_update


if __name__ == '__main__':
    app.layout = layout
    app.run_server()

