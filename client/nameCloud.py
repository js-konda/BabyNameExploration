import base64
from io import BytesIO

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from wordcloud import WordCloud

from app import app, df

layout = html.Div([
    dcc.Graph(id='name-cloud-graph',
              config = {'displayModeBar':False, 'staticPlot':True}),

    html.Div([
            html.Div([
                html.Div([
                    'TOP',
                    dcc.Slider(1, 150, 10,
                               # marks=None,
                               value=50,
                               id='name-cloud-input-th'),
                ],
                    style={'width': '500px',
                           # 'display': 'inline-block',
                           'padding': '0px',
                           'margin': '0 auto'
                           }
                ),

                html.Div([
                    'Year  ',
                    dcc.Input(id='name-cloud-input-year', type='number', value=2020)
                ],
                    style={'width': '500px',
                           # 'display': 'inline-block',
                           'padding': '0px',
                           'margin': '0 auto',
                           # 'position': 'absolute',
                           # 'left': '310px',
                           }
                ),

                html.Div(
                    id='name-cloud-graph-alert',
                    children=[],
                    style={
                           # 'display': 'inline-block',
                           'position': 'absolute',
                           'height': '50px',
                           'left': '200px',
                            'top': '60px'
                           }
                ),

                html.Div([
                    dcc.RadioItems(
                        id='name-cloud-input-sex',
                        options=[
                            {'label': 'Female', 'value': 'F'},
                            {'label': 'Male', 'value': 'M'},
                        ],
                        value='F'
                    )
                ],
                style={'width': '150px',
                      # 'display': 'inline-block',
                      'margin': '0 auto',
                      'margin-top':'4px'
                      # 'position': 'absolute',
                      # 'top':'90px',
                      # 'left': '500px',
                }),

            ],
            style={
                'margin':'0 auto',
                'position':'relative',
                'width':'500px'
            })
    ]),
],

)

alert = dbc.Alert("Please input year between 1910-2020!", color='danger', dismissable=False, duration=1500)

@app.callback(
    Output('name-cloud-graph', 'figure'),
    Output('name-cloud-graph-alert', 'children'),
    Input('name-cloud-input-year', 'value'),
    Input('name-cloud-input-sex', 'value'),
    Input('name-cloud-input-th', 'value')
)

def update_figure(year, sex, th):
    if year not in df.year.values and year != None:
        return [], alert
    year = int(year)
    th = int(th)

    filtered_df = df[df['year'] == year]
    filtered_df = filtered_df[filtered_df['sex'] == sex]
    names = filtered_df[['name', 'count']].groupby('name').sum()
    sort_names = names.sort_values(by='count', ascending=False)
    sort_names_th = sort_names.head(th)
    most_named = pd.Series(sort_names_th['count'].values, index=sort_names_th.index).to_dict()

    wc = WordCloud(background_color="white",
                   random_state=42, width=1500, height=1500)
    nc = wc.generate_from_frequencies(most_named)
    nc_img = nc.to_image()
    prefix = "data:image/png;base64,"
    with BytesIO() as buffer:
        nc_img.save(buffer, 'png')
        img2 = prefix + base64.b64encode(buffer.getvalue()).decode()

    fig = go.Figure(go.Image(source=img2))
    return fig, dash.no_update


if __name__ == '__main__':
    app.layout = layout
    app.run_server()
