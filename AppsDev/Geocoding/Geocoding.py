# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 09:05:45 2018

@author: jingwenken
"""
from geopy import Nominatim

nom = Nominatim(scheme="http")

loc = nom.geocode('Chicago Illinois',timeout=30)
print(loc.latitude, " ", loc.longitude)


"""
try:
    location = nom.geocode("3995 23rd St, San Francisco, CA94119",timeout=10)
    print (location.longtitude,location.latitude)
except GeocoderTimedOut as e:
    print("Error: msg is error")
"""    