# index.py

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

# must add this line in order for the app to be deployed successfully on Heroku
from app import server
from app import app
# import all pages in the app
from apps import home,stat

navbar = dbc.NavbarSimple(
        children=[
        dbc.NavItem(dbc.NavLink("Stats", href="/stat")),
    ],
    style={'fontSize': 22},
    
    brand="ContraViz - A Global COVID-19 Trend Tracking Visualizer",
    brand_href="/home",
    brand_style={'fontSize': 30},
    color="dark",
    dark=True,
    fluid=True,
    #sticky="top",
)
 
# embedding the navigation bar
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])

def display_page(pathname):
    if pathname == '/stat':
        return stat.layout
    else:
        return home.layout
    
    #dev_tools_hot_reload = False

if __name__ == '__main__':
    app.run_server(debug=True)
