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
import plotly.graph_objs as go

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
        'background': '#0000FF',
        'text': '#FFFFFF'
        }
header = {
        'textAlign' : 'center'
        }

## App Layout

go.Scatter(
    x = [0.1*len(data['VOBC'])],
    y = data['VOBC'],
    mode='lines'
    )

app.layout = html.Div(style=colors, children=[
        html.H1(style=header,children='CBTC Visualisation'),
        html.Div(style=header,children='Built by CTMO'),
        html.Div(
                dcc.Graph(
                        id = 'Overview Plot',
                        figure = {
                                'data' : [
                                        go.Bar(
                                            x= data[(data[' Date']==last_date) & (data['VOBC']==i)]['VOBC'],
                                            #y= data[(data[' Date']==last_date) & (data['VOBC']==i)]['Dev'],
                                            y= list(range(1,data[(data[' Date']==last_date)].shape[0])),
                                            name = 'VOBC '+ str(i),
                                            showlegend = False
                                            ) for i in data[data[' Date']==last_date]['VOBC']
                                        ]+[
                                        go.Scatter(
                                            x = data['VOBC'],
                                            y = [0.1]*len(data['VOBC']),
                                            mode='lines'
                                            )
                                        ],
                                'layout' : go.Layout(
                                        xaxis={'title': 'VOBC'},
                                        yaxis={'title': 'Deviation'},
                                        hovermode='closest'
                                        )
                        }
                )
        )
])

'''
#Massive Line plot of all EMUs
dcc.Graph(
                    id='Overview Plot',
                    figure={
                            'data' : [
                                    go.Scatter(
                                        x=data[data['VOBC']==i][' Date'],
                                        y=data[data['VOBC']==i]['Dev'],
                                        mode='markers+lines',
                                        opacity=0.7,
                                        marker={
                                                'size' : data[data['VOBC']==i]['Dev']*3,
                                                'line' : {'width': 0.5, 'color': 'white'}
                                                },
                                        name = str('VOBC ' + str(i))
                                        ) for i in data['VOBC'].unique()
                                    ],
                            'layout': go.Layout(
                                    height= 1000,
                                    xaxis={'title': 'Date'},
                                    yaxis={'title': 'Deviation'},
                                    hovermode='closest'
                                    )
                            }
        )
'''

if __name__ == '__main__':
    app.run_server(debug=True)