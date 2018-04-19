# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 14:23:33 2018

@author: jingwenken
"""

import folium
import pandas

volcanos = pandas.read_csv('Volcanoes_USA.txt')
lat = list(volcanos["LAT"])
lon = list(volcanos["LON"])
name = list(volcanos["NAME"])
elev = list(volcanos["ELEV"])

map1 = folium.Map(location=[38.58,-99.09],zoom_start=6)

#function to map elevation to color
def color_producer(elev):
    if elev < 1567:
        return 'green'
    elif 1567 <= elev < 2787:
        return 'orange'
    else:
        return 'red'

#adding markers to the map
fg1 = folium.FeatureGroup(name="Points")
for lt,ln,nme,ele in zip(lat,lon,name,elev):
    fg1.add_child(folium.CircleMarker(location=[lt,ln],
                 popup=folium.Popup(str(nme),
                 parse_html=True),
                 fill=True,
                 fill_color=color_producer(ele),
                 color='grey',
                 fill_opacity=1))
 
#adding another layer to the map
fg2 = folium.FeatureGroup(name="Pop Color")
fg2.add_child(folium.GeoJson(data=open('world.json','r',encoding='utf-8-sig').read(),
            style_function=lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 10000000
                                      else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000
                                      else 'red'}))

map1.add_child(fg1)
map1.add_child(fg2)
#adds ability to toggle the different features on/off on the web map
map1.add_child(folium.LayerControl())

map1.save("Map1.html")