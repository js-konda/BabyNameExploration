import dash_html_components as html
from app import app

parentLayout = html.Div([])

app.layout = parentLayout

app.run_server()
