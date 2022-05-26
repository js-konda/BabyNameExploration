import pandas as pd
from dash import Dash
import dash_bootstrap_components as dbc
import os
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'baby-names-state.csv')

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
df = pd.read_csv(filename)
