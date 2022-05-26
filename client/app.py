import pandas as pd
from dash import Dash
import os
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'baby-names-state.csv')

app = Dash(__name__)
df = pd.read_csv(filename)
