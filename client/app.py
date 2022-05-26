import pandas as pd
from dash import Dash

app = Dash(__name__)
df = pd.read_csv(r'baby-names-state.csv')