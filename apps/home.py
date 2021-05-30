#!/usr/bin/env python
# coding: utf-8

# importing libraries
import pandas as pd
import numpy as np

import plotly
import plotly.express as px
import plotly.graph_objs as go

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import dash_table

# read data from John Hopkins github repo
df = pd.read_csv('https://raw.githubusercontent.com/datasets/covid-19/main/data/countries-aggregated.csv')

df['Active'] = df['Confirmed'] - df['Deaths'] - df['Recovered']

date_agg = df.groupby('Date')['Confirmed','Recovered', 'Active', 'Deaths'].sum().reset_index()
date_agg = date_agg.melt(id_vars="Date", value_vars=['Confirmed', 'Recovered', 'Active', 'Deaths'],
                 var_name='Case', value_name='Count')

country = df.groupby('Country').sum().reset_index()

current = date_agg.Date.iloc[-1]
top = df[df.Date == current]

#Overwrite your CSS setting by including style locally
colors = {
    'confirmed_text':'#3CA4FF',
    'deaths_text':'#f44336',
    'recovered_text':'#5A9E6F',
    'active_text': '#FFFF00',    
}

first_card = dbc.Card(
    dbc.CardBody(
        [
            html.H4('Confirmed Cases', className="card-title", style={ 'textAlign': 'center','color': colors['confirmed_text'], 'margin-bottom' : 0, 'margin-top' : 5,}),
            html.P(f"{date_agg.Count[date_agg.Case == 'Confirmed'].iloc[-1]:,d}",
                       style={
                    'textAlign': 'center',
                    'color': colors['confirmed_text'],
                    'fontSize': 30,
                    'margin-bottom' : 0,}
                  ),
        ]))


second_card = dbc.Card(
    dbc.CardBody(
        [
            html.H4('Recovered Cases', className="card-title", style={ 'textAlign': 'center','color': colors['recovered_text'], 'margin-bottom' : 0,  'margin-top' : 5, }),
            html.P(f"{date_agg.Count[date_agg.Case == 'Recovered'].iloc[-1]:,d}",
                       style={
                    'textAlign': 'center',
                    'color': colors['recovered_text'],
                    'fontSize': 30,
                       'margin-bottom' : 0,}
                  ),
        ]))

third_card = dbc.Card(
    dbc.CardBody(
        [
            html.H4('Death Cases', className="card-title", style={ 'textAlign': 'center','color': colors['deaths_text'],'margin-bottom' : 0, 'margin-top' : 5, }),
            html.P(f"{date_agg.Count[date_agg.Case == 'Deaths'].iloc[-1]:,d}",
                       style={
                    'textAlign': 'center',
                    'color': colors['deaths_text'],
                    'fontSize': 30,
                    'margin-bottom' : 0,
                }
                ),
        ]))

fourth_card = dbc.Card(
    dbc.CardBody(
        [
            html.H4('Active Cases', className="card-title", style={ 'textAlign': 'center','color': colors['active_text'], 'margin-bottom' : 0, 'margin-top' : 5,}),
            html.P(f"{date_agg.Count[date_agg.Case == 'Active'].iloc[-1]:,d}",
                       style={
                    'textAlign': 'center',
                    'color': colors['active_text'],
                    'fontSize': 30,
                    'margin-bottom' : 0,}
                  ),
        ]))


cards = dbc.Row([dbc.Col(first_card, width=3), dbc.Col(second_card, width=3), dbc.Col(third_card, width=3), dbc.Col(fourth_card, width=3)],style={'margin': 20})

################## DASH TABLE ###########################3

# Dash Data table
table = dash_table.DataTable(

    columns=[{"name": i, "id": i} for i in country.columns],
    data=country.to_dict('records'),
    
    fixed_rows={'headers': True},
    
    style_header={'backgroundColor': 'black', 'color': 'white', 'fontWeight': 'bold'},
    
    style_cell={
        'color': 'black',
        'fontWeight': 'bold',
        'minWidth': 5, 'maxWidth': 25, 'width': 15,  'whiteSpace': 'normal',
        'height': 'auto',
    },
    
    style_cell_conditional=[
        {'if': {'column_id': 'Country'},
         'width': '35%', 'text-align':'left', 
         'backgroundColor': '#EEEEEE'},
        
        {'if': {'column_id': 'Confirmed'},
         'backgroundColor': '#87CEEB'},
        
        {'if': {'column_id': 'Recovered'},
         'backgroundColor': '#5A9E6F'},
        
        {'if': {'column_id': 'Deaths'},
         'backgroundColor': '#ff7f7f'},
        
        {'if': {'column_id': 'Active'},
         'backgroundColor': '#FFFCBB'},
    
    ],
    page_action='none',
    style_table={ 'height': '500px', 'overflowY': 'auto',},
    
    
    ########### 'height': '500px', 'width': '450px',
    style_as_list_view=True,
)

################### GLOBE ######################

def globe() :
    fig = px.choropleth( top, locations="Country",
                        color="Confirmed", 
                        hover_name="Country", 
                        hover_data=[ 'Confirmed','Deaths','Recovered','Active'], 
                        locationmode="country names",
                        projection="orthographic",
                        color_continuous_scale="Sunsetdark",
                        range_color=[1,15000000],
                        height=500,
                        #width=700,
                       ).update_layout(template="plotly_dark",coloraxis_showscale=True, margin=dict(l=0, r=0, t=25, b=25),
                    geo=dict(showcoastlines=False,showocean=True, oceancolor="LightBlue",),
                    )
    return fig

#paper_bgcolor='rgba(0,0,0,0)'
######################## APP LAYOUT ###################################

layout = html.Div(
    [
     cards, 
     html.Br(),
     
     dbc.Row([ 
             dbc.Col([
                     html.H6("Total cases till date", className="text-center"),
                     table,
                     ], width=5, style={ 'margin-left' : 30, 'margin-right' : 10,}),
            
            dbc.Col([
                      html.H6("Total cases till date", className="text-center"),
                      
                     #earth graph
                     dcc.Graph(
                             figure = globe() ,
                              ),
                             #config={'displayModeBar': False}    for plotly options like  reset axes
                             ], width = 6,
                    ),
        
    ],),
    html.Br(),
    ]
    )

