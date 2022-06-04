import numpy as np
import pandas as pd
import os
import plotly.graph_objects as go
import dash
import dash_bootstrap_components as dbc


def test_topName():
    from client.top5Name import update_figure
    res = update_figure(1800, 2020, 'M', 5, 'CA')
    assert isinstance(res[0], list)
    assert isinstance(res[1], dbc.Alert)
    res1 = update_figure(2000, 2020, 'M', 5, 'CA')
    assert isinstance(res1[0], go.Figure)
    assert isinstance(res1[1], dash._callback.NoUpdate)
    
def test_nameCloud():
    from client.nameCloud import update_figure
    res = update_figure(1800, 1800, 15, 'CA')
    assert isinstance(res[0], list)
    assert isinstance(res[1], dbc.Alert)
    res1 = update_figure(2020, 2020, 15, 'CA')
    assert isinstance(res1[0], go.Figure)
    assert isinstance(res1[1], dash._callback.NoUpdate)
    
def test_nameCloud_most_named():
    from client.nameCloud import get_most_named_data
    res = get_most_named_data(2020, 2020, 15, 'M', 'CA')
    assert isinstance(res, dict)
    
def test_nameTrend():
    from client.nameTrend import update_figure
    res = update_figure('sdjhidrefnk', 'M', 'CA')
    assert isinstance(res[0], list)
    assert isinstance(res[1], dbc.Alert)
    res1 = update_figure('Jack', 'M', 'CA')
    assert isinstance(res1[0], go.Figure)
    assert isinstance(res1[1], dash._callback.NoUpdate)
    
def test_heatmap():
    from client.USHeatMap import update_figure
    res = update_figure('Jack', 'M', 1800)
    assert isinstance(res[0], dict)
    assert isinstance(res[1], dbc.Alert)
    assert isinstance(res[2], dash._callback.NoUpdate)
    res1 = update_figure('sdjhidrefnk', 'M', 2000)
    assert isinstance(res1[0], dict)
    assert isinstance(res1[2], dbc.Alert)
    assert isinstance(res1[1], dash._callback.NoUpdate)
    res2 = update_figure('Jack', 'M', 2000)
    assert isinstance(res2[0], dict)
    assert isinstance(res2[1], dash._callback.NoUpdate)
    assert isinstance(res2[2], dash._callback.NoUpdate)
    
def test_genderClassifier():
    from client.genderClassifier import update_figure
    res = update_figure('Jack')
    assert isinstance(res, go.Figure)
    
    