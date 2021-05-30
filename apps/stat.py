# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 01:56:29 2021

@author: KARTIK
"""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import dash  # (version 1.12.0) 
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from raceplotly.plots import barplot
from matplotlib import animation as F
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.style as style
from random import randint
import random

from app import app
from apps import home

df=home.df
date_agg=home.date_agg

scale = {
    'Confirmed':"deep",
    'Deaths':"reds",
    'Recovered':"dense",
    'Active': "ylgn",
}

########### Layout #############
layout = dbc.Container([

     dbc.Row([
             html.Br(),
        dbc.Col([
            html.Br(), html.Br(),
            dcc.Dropdown(id='my-dpdn', multi=False, value='India',
                         options=[{'label':x, 'value':x}
                                  for x in sorted(df['Country'].unique())], 
                         ),
            
            dcc.Graph(id='line-fig', figure={})
                      
        ], width={'size':6, 'order':1},
           #xs=12, sm=12, md=12, lg=5, xl=5
        ),

        dbc.Col([
                   
            dcc.RadioItems(id='my-radio', value='Confirmed',
                          options=[{'label': 'Confirmed', 'value':'Confirmed'}, {'label': 'Active', 'value':'Active'}, 
                                   {'label': 'Deaths', 'value':'Deaths'}, {'label': 'Recovered', 'value':'Recovered'}],
                          labelClassName="mr-4",                          
                          labelStyle={'display': 'inline-block','mt':10,'fontSize': 20,},
                          ),            
            
            dcc.Dropdown(id='my-dpdn2', multi=True, value=['US','India'],
                         options=[{'label':x, 'value':x}
                                 for x in sorted(df['Country'].unique())],
                         ),
                          
            dcc.Graph(id='line-fig2', figure={})
        ], width={'size':6, 'order':2},
           # xs=12, sm=12, md=12, lg=5, xl=5
        ),

    ],  no_gutters=False, justify='start'),
                          
                          
     dbc.Row([
        dbc.Col(dbc.Card(html.H5(children='Top 10 Most Affected Countries Over Time',
                                 className="text-center text-light bg-dark"), body=True, color="dark")
        , className="mt-1 mb-1")
    ]),

    dbc.Row([
            
            dbc.Col([
                    dcc.RadioItems(id='my-radio2', value='Confirmed',
                          options=[{'label': 'Confirmed', 'value':'Confirmed'}, {'label': 'Active', 'value':'Active'}, {'label': 'Deaths', 'value':'Deaths'}, {'label': 'Recovered', 'value':'Recovered'}],
                          labelClassName="mr-4",
                          labelStyle={'display': 'inline-block','mt':10,'fontSize': 20,},
                          ),
            
        ], width={'size':6, 'order':3},
           # xs=12, sm=12, md=12, lg=5, xl=5
        )
    ]),
    dcc.Graph(id='line-fig3', figure={}),

    dbc.Row([
        dbc.Col(dbc.Card(html.H5(children='Heatmap showing the extent of each type of case across the globe',
                                 className="text-center text-light bg-dark"), body=True, color="dark")
        , className="mt-1 mb-1")
    ]),

    dbc.Row([

        dbc.Col([
            dcc.RadioItems(id='my-radio3', value='Confirmed',
                          options=[{'label': 'Confirmed', 'value':'Confirmed'}, {'label': 'Active', 'value':'Active'}, {'label': 'Deaths', 'value':'Deaths'}, {'label': 'Recovered', 'value':'Recovered'}],
                          labelClassName="mr-4",
                          labelStyle={'display': 'inline-block','mt':10,'fontSize': 20,},),
            dcc.Graph(id='line-fig4', figure={})
        ], width={'size':6, 'offset': 1, 'order':4},
           #xs=12, sm=12, md=12, lg=5, xl=5
        )
    ], )

], fluid=True)

@app.callback(
    Output('line-fig', 'figure'),
    Input('my-dpdn', 'value')
)

# option_slctd

def update_graph(country):
    country_confirm = df.Confirmed[df.Country == country]
    country_deaths = df.Deaths[df.Country == country]
    country_recovery = df.Recovered[df.Country == country]
    country_active = df.Active[df.Country == country]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=date_agg.Date, y=country_confirm, mode='lines', name='Confirmed Cases',))
    fig.add_trace(go.Scatter(x=date_agg.Date, y=country_deaths, mode='lines', name='Deaths',))
    fig.add_trace(go.Scatter(x=date_agg.Date, y=country_recovery, mode='lines', name='Recovered Cases'))
    fig.add_trace(go.Scatter(x=date_agg.Date, y=country_active, mode='lines', name='Active Cases'))
                             
   
    fig.update_layout( template = "plotly_dark", hovermode="x",margin=dict(l=35, r=35, t=0, b=35),
                      legend=dict( x=0.02, y=1,), height=300,
                     )
    fig.update_xaxes(showgrid=False, gridwidth=1, gridcolor='#3A3A3A')
    fig.update_yaxes(showgrid=False, gridwidth=1, gridcolor='#3A3A3A')

    fig.update_yaxes(zeroline=True, zerolinewidth=2, zerolinecolor='#3A3A3A')
                     
    return fig


@app.callback(
    Output('line-fig2', 'figure'),
    Input('my-radio', 'value'),
    Input('my-dpdn2', 'value')
)
def update_graph(check_type, country):
   # check_type = check_opt
    #country = option_slctd
    country_type = df[df['Country'].isin(country)]
    country_type = pd.pivot_table(country_type, values=check_type, index=['Date'], columns='Country')
    
    fig = go.Figure()
    for col in country_type.columns:
        fig.add_trace(go.Scatter(x=country_type.index, y=country_type[col].values,name=col, mode='lines'))
    
    fig.update_layout( template = "plotly_dark", hovermode="x", margin=dict(l=35, r=35, t=0, b=35),
                      legend=dict( x=0.02, y=1,), height=300, 
                     )
    fig.update_xaxes(showgrid=False, gridwidth=1, gridcolor='#3A3A3A')
    fig.update_yaxes(showgrid=False, gridwidth=1, gridcolor='#3A3A3A')
    return fig


@app.callback(
    Output('line-fig3', 'figure'),
    Input('my-radio2', 'value')
)

def update_graph(check_opt):
    check_opt = str(check_opt)
   
    fig = barplot(df,  item_column='Country', value_column=check_opt, time_column='Date') #item_color='color')
    return fig.plot(item_label = 'Top 10 countries', value_label = 'Date', frame_duration = 1)


@app.callback(
    Output('line-fig4', 'figure'),
    Input('my-radio3', 'value')
)

def update_graph(check_opt):
    check_opt = str(check_opt)
    
    fig = px.choropleth(df, locations="Country", locationmode='country names', color=check_opt, width = 1100, height= 600, hover_name="Country", range_color=[1,15000000], animation_frame = 'Date', color_continuous_scale=scale[check_opt], title= (check_opt + ' Cases Worldwide'))
    
    fig = fig.update_layout( template = "plotly_dark", font_color='#FFF', margin=dict(l=15, r=5, t=40, b=0), title={'y':0.97,'x':0.5,'xanchor': 'center','yanchor': 'top'}, transition = {'duration': 1})
    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1
    return fig
