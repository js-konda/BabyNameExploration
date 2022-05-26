import dash_html_components as html
from app import app
import nameTrend
import top5Name
import USHeatMap

parentLayout = html.Div([nameTrend.layout, top5Name.layout, USHeatMap.layout])

app.layout = parentLayout

app.run_server()
