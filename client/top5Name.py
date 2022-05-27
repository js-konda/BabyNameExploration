import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output

from app import app, df

layout = html.Div([
    dcc.Graph(id='top5-name-graph'),

    html.Div([
            html.Div([
                html.Div([
                    'TOP',
                    dcc.Slider(1, 20, 1,
                               # marks=None,
                               value=5,
                               id='top5-name-input-th'),
                ],
                    style={'width': '500px',
                           # 'display': 'inline-block',
                           'padding': '0px',
                           'margin': '0 auto'
                           }
                ),

                html.Div([
                    'Year  ',
                    dcc.Input(id='top5-name-input-year', type='number', value=2020)
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
                    id='top5-name-the-alert',
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
                        id='top5-name-input-sex',
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
    Output('top5-name-graph', 'figure'),
    Output('top5-name-the-alert', 'children'),
    Input('top5-name-input-year', 'value'),
    Input('top5-name-input-sex', 'value'),
    Input('top5-name-input-th', 'value')
)

def update_figure(year, sex, th):
    if year not in df.year.values and year != None:
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
    app.layout = layout
    app.run_server()
