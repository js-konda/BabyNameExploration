import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html

import client.USHeatMap as USHeatMap
import client.genderClassifier as genderClassifier
import client.nameCloud as nameCloud
import client.nameTrend as nameTrend
import client.top5Name as top5Name
from client.app import app

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.P(
            "US Newborn Naming Analysis", className="lead"
        ),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Top Names", id="link-top5", href="/", active="exact"),
                dbc.NavLink("US Name Cloud", id="link-name-cloud", href="/name-cloud", active="exact"),
                dbc.NavLink("Name Trend", id="link-name-trend", href="/name-trend", active="exact"),
                dbc.NavLink("US Heat Map", id="link-heat-map", href="/heat-map", active="exact"),
                dbc.NavLink("Gender Classifier", id="link-gender-classifier", href="/gender-classifier", active="exact")
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
    id="content-sidebar"
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    layout, code = page_router(pathname)
    return layout


def page_router(pathname):
    if pathname == "/":
        return top5Name.layout, 200
    elif pathname == "/name-cloud":
        return nameCloud.layout, 200
    elif pathname == "/name-trend":
        return nameTrend.layout, 200
    elif pathname == "/heat-map":
        return USHeatMap.layout, 200
    elif pathname == "/gender-classifier":
        return genderClassifier.layout, 200
    # If the user tries to reach a different page, return a 404 message
    return top5Name.layout, 404


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=False, port=8050)
