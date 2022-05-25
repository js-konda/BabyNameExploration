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
from plotly.subplots import make_subplots
import plotly.offline as py
from plotly.offline import init_notebook_mode
init_notebook_mode(connected=True)
from dash.dependencies import Input, Output

app = Dash(__name__)
df = pd.read_csv(r'baby-names-state.csv')

app.layout = html.Div([
    html.Div([
        dcc.Graph(id='trend-graph'),
        html.Div([
            'Year',
            dcc.Slider(1910, 2020, 1,
                       marks=None,
                       value=2020,
                       id='input-year'),
        ],
            style={'width': '500px',
                   # 'display': 'inline-block',
                   'padding': '0px',
                   'margin': '0 auto'
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
        style={'width': '180px',
               # 'display': 'inline-block',
               'padding': '0px',
               'margin': '0 auto'
               }
        ),
        html.Div([
            dcc.Input(id='input-name', value='Oliver', type='text')
        ],
        style={'width': '200px',
               'padding': '0px',
               'margin': '15px auto'
               }
        ),
    ]),

])



@app.callback(
    Output('trend-graph', 'figure'),
    Input('input-name', 'value'),
    Input('input-sex', 'value'),
    Input('input-year', 'value')
)


def update_figure(name,sex, year):
    year = int(year)
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
    return fig

if __name__ == '__main__':
    app.run_server()

