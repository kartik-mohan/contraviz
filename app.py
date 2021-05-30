# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 01:12:20 2021

@author: KARTIK
"""

import dash
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
app.title = 'ContraViz '

server = app.server

app.config.suppress_callback_exceptions = True