# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 22:14:03 2018

@author: Mezu
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np


#Let's read in data and parse the Date field into Datetime
df_water_quality = pd.read_csv(
    'https://raw.githubusercontent.com/charleyferrari/CUNY_DATA_608/'
    'master/module4/Data/riverkeeper_data_2013.csv',parse_dates=['Date'])

#Convert datetime to date string in Year, month day for sorting
df_water_quality['Date_str']=df_water_quality['Date'].dt.strftime('%Y-%m-%d')
df_water_quality['Date']= pd.to_datetime(df_water_quality['Date'])


# We notice some '<' and '>' signs in the Enterocount column. Let's replace them

#for '<' Let's find those values
dummy=df_water_quality[df_water_quality['EnteroCount'].str.startswith('<', na=False)].EnteroCount.unique()


#we can see that it is <1 and <10  are the values we need to replace that have <
df_water_quality['EnteroCount'].replace(to_replace = "<10", value = 9, inplace = True)
df_water_quality['EnteroCount'].replace(to_replace = "<1", value = 0, inplace = True)

#for '>' Let's find those values
dummy2=df_water_quality[df_water_quality['EnteroCount'].str.startswith('>', na=False)].EnteroCount.unique()

#we can see that it is >2420 and >24196 are the values we need to replace that have <
df_water_quality['EnteroCount'].replace(to_replace = ">2420", value = 2421, inplace = True)
df_water_quality['EnteroCount'].replace(to_replace = ">24196", value = 24197, inplace = True)

#Ensure that the field is numeric
df_water_quality['EnteroCount'] = pd.to_numeric(df_water_quality['EnteroCount'])
df_water_quality['FourDayRainTotal'] =pd.to_numeric(df_water_quality['FourDayRainTotal'])

app = dash.Dash()

available_indicators = df_water_quality['Site'].unique()

app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='site',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Pier 96 Kayak Launch'
            ),
            
        ],
        style={'width': '48%', 'display': 'inline-block'})

    ]),

    dcc.Graph(id='indicator-graphic')
])


@app.callback(
    dash.dependencies.Output('indicator-graphic', 'figure'),
    [dash.dependencies.Input('site', 'value')])
def update_graph(site_name):
    dff = df_water_quality[df_water_quality['Site'] == site_name]

    return {
        'data': [go.Scatter(
            x=dff['FourDayRainTotal'],
            y=dff['EnteroCount'],
            text=dff['Date'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': 'FourDayRainTotal',
                'type': 'linear' 
            },
            yaxis={
                'title': 'EnteroCount',
                'type': 'linear' 
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }


if __name__ == '__main__':
    app.run_server()