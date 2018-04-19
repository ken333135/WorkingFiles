# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 10:18:56 2018

@author: jingwenken
"""
import pandas
from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource, HoverTool, LabelSet
from bokeh.plotting import figure
from bokeh.palettes import Spectral5
from bokeh.sampledata.autompg import autompg_clean as df
from bokeh.transform import factor_cmap
from bokeh.palettes import d3

output_file("bars.html")
df=pandas.read_csv('simulated_data.csv')

groupby1 = 'character'
groupby2 = 'class'

group = df.groupby((groupby1,groupby2))
grpby_string = groupby1 + '_' + groupby2
count_string = group.describe().columns[0][0] + '_count'

source = ColumnDataSource(group)
index_cmap = factor_cmap(grpby_string, palette=Spectral5, factors=sorted(df[groupby1].unique()), end=1)

hover=HoverTool(tooltips=[
        ("count",'@'+count_string)])

p = figure(plot_width=800, plot_height=300, title="Mean MPG by # Cylinders and Manufacturer",
           x_range=group, toolbar_location=None, tools=[hover])

labels=LabelSet(x=grpby_string,text=count_string,level='glyph',source=source,y_offset=50,x_offset=-5)


p.vbar(x=grpby_string, top=count_string, width=1, source=source,
       line_color="white", fill_color=index_cmap)

p.add_layout(labels)
p.y_range.start = 0
p.x_range.range_padding = 0.05
p.xgrid.grid_line_color = None
p.xaxis.axis_label = "Manufacturer grouped by # Cylinders"
p.xaxis.major_label_orientation = 1.2
p.outline_line_color = None

show(p)

