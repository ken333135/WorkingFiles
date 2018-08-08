# -*- coding: utf-8 -*-
"""
Created on Fri Aug  3 10:04:39 2018

@author: jingwenken
"""
#%%
import pandas as pd
import numpy as np
from datetime import datetime

def parse_date(date):
    return datetime.strptime(date, '%Y%m%d')
    
data_path = r'C:\Users\jingwenken\Desktop\Ken\CTMO\SnC_RDB_Data\20180529\BSD-DIAG\Hist_Data\Accelerometer\MedianAccelerationsHist.csv'
data = pd.read_csv(data_path,parse_dates=[3],date_parser=parse_date)
data[' Acc0'] = data[' Acc0'].replace(' nan',0)
data[' Acc1'] = data[' Acc1'].replace(' nan',0)
data[' Acc0'] = pd.to_numeric(data[' Acc0'])
data[' Acc1'] = pd.to_numeric(data[' Acc1'])
data = data.fillna(0)

#add column for Rsquared deviation
data['Dev'] = np.sqrt((data[' Acc0']**2)+(data[' Acc1']**2))

#get the latest date
last_date = data[' Date'].max()
#%%

#### End of Data Processing ####

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import json
from textwrap import dedent as d

app = dash.Dash()

## External CSS
external_css = ["https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css",
              "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" ]
for css in external_css:
    app.css.append_css({"external_url": css})

## External JavaScript
external_js = ["http://code.jquery.com/jquery-3.3.1.min.js",
               "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"]
for js in external_js:
    app.scripts.append_script({"external_url": js})

## Internal CSS
colors = {
        'background': '#FFFFFF',
        'text': '#FFFFFF'
        }
header = {
        'textAlign' : 'center'
        }
fixed_forecast = {
        'position' : 'fixed',
        'top' : '90px',
        'left': '720px'
        }
fixed_axis = {
        'position' : 'fixed',
        'top' : '90px',
        'left': '1250px'
        }

custom_colorscale = [
    [0.00, 'rgb(166,206,227)'], 
    [0.25, 'rgb(31,120,180)'], 
    [0.45, 'rgb(178,223,138)'], 
    [0.65, 'rgb(51,160,44)'], 
    [0.85, 'rgb(251,154,153)'], 
    [1.00, 'rgb(227,26,28)']
]

#App function definitions

def row(children):
    return html.Div(children, className='row')

fleet_graph = dcc.Graph(
                    id = 'fleet-view',
                    style = {
                            'height' : len(data['VOBC'].unique())*12,
                            'width': len(data[' Date'].unique())*12
                            },
                    figure = {
                            'data' : [
                                    go.Scatter(
                                        x = data[data['VOBC']==i][' Date'],
                                        y = [n]*data[data['VOBC']==i].shape[0],
                                        hovertext = ['{:4f}</br>VOBC: {}'.format(j,i) for j in data[data['VOBC']==i]['Dev'].values.tolist()],
                                        mode = 'markers',
                                        name = 'Deviation',
                                        marker=dict(
                                            size=10, #size=size,
                                            color=data[data['VOBC']==i]['Dev'].values.tolist(), # assign colors by size
                                            colorscale=custom_colorscale, #'Jet', #'Viridis',
                                            opacity = 0.75,
                                            line=dict(color='rgb(140, 140, 170)')
                                        ),
                                    ) for n, i in enumerate(data['VOBC'].unique())
                                
                                    ],
                            'layout' : go.Layout(
                                    showlegend=False,
                                    yaxis=dict(
                                        autorange=True,
                                        showgrid=False,
                                        zeroline=False,
                                        showline=False,
                                        showticklabels=False,
                                    ),
                                    hovermode='closest',
                                    margin=go.Margin(l=20, r=0, t=0, b=0)
                                    )
                                }
                        )

## App Layout    

app.layout = html.Div(style=colors, children=[
        html.H1(style=header,children='CBTC Visualisation'),
        html.H4(style=header,children='Built by CTMO'),
        row([html.Div(
                    className = 'six columns',
                    id = 'fleet-view-container',
                    children = [
                            html.H3(style=header,children='Fleet View'),
                            fleet_graph
                            ]
                    ),
            html.Div(
                    className = 'three columns',
                    id = 'forecast-view-container',
                    style=fixed_forecast,
                    children=[
                            html.H3(style=header,children='Forecast View'),
                            dcc.Graph(id='forecast-view')
                            ]
                    ),
            html.Div(
                    className = 'three columns',
                    id = 'axis-view-container',
                    style=fixed_axis,
                    children=[
                            html.H3(style=header,children='Axis View'),
                            dcc.Graph(id='axis-view')
                            ]
                    )
        ])
])

#Forecast Graph
def create_forecast(df,vobc):
    return {
            'data': [go.Scatter(
                        x = df[' Date'],
                        y = df['Dev'],
                        mode = 'lines+markers',
                        name = 'VOBC '+str(vobc)
                    )]+[go.Scatter(
                            x = df[' Date'], 
                            y = [0.1]*len(df[' Date']),
                            mode= 'lines',
                            name = 'Threshold'
                        )],
            'layout': {
                'height': 600,
                'width' : 500,
                'showlegend' : False,
                'title' : 'VOBC '+str(vobc)
            }
        }
    
@app.callback(Output('forecast-view', 'figure'),
              [Input('fleet-view', 'clickData')])
def update_forecast(clickData):
    info = clickData['points'][0]['hovertext']
    vobc = int(info.split('VOBC: ')[1])
    print(vobc)
    df = data[data['VOBC']==vobc]
    return create_forecast(df,vobc)

#Axis Graph

def create_axis(df):
    return {
        'data' : [go.Scatter(
                    x = [df.loc[i][' Acc0']],
                    y = [df.loc[i][' Acc1']],
                    mode = 'lines+markers',
                    name = datetime.strftime(df.loc[i][' Date'],'%d %b %Y'),
                    text = "{:05.3f},{:05.3f}".format(df.loc[i][' Acc0'],df.loc[i][' Acc1']),
                    marker=dict(
                        color='red',
                        opacity=n/len(df.index)
                        )
                    ) for n,i in enumerate(df.index)],
        'layout' : {
            'height' : 600,
            'width' : 500,
            'showlegend' : False,
            'shapes' :[
                    {
                        'type':'circle',
                        'xref':'x',
                        'yref':'y',
                        'x0':-0.1,
                        'y0':-0.1,
                        'x1':0.1,
                        'y1':0.1,
                        'line': {'color':'lightgrey', 'width':2, 'dash':'dot'}
                    }
            ]
        }
    }


@app.callback(Output('axis-view', 'figure'),
              [Input('fleet-view', 'clickData')])
def update_axis(clickData):
    info = clickData['points'][0]['hovertext']
    vobc = int(info.split('VOBC: ')[1])
    df = data[data['VOBC']==vobc]
    return create_axis(df)

if __name__ == '__main__':
    app.run_server(debug=True)