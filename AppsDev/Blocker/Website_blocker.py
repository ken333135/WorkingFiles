# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 15:52:06 2018

@author: jingwenken
"""

import time
import datetime

host_temp=r"hosts"
host_path="C:\Windows\System32\drivers\etc\hosts"
redirect="127.0.0.1"
website_list=["facebook.com","www.facebook.com"]

start = datetime.datetime(datetime.datetime.now().year,datetime.datetime.now().month,datetime.datetime.now().day,8)
end = datetime.datetime(datetime.datetime.now().year,datetime.datetime.now().month,datetime.datetime.now().day,18)

while True:
    if start < datetime.datetime.now() < end:
        with open(host_temp,'r+') as file:
            content=file.read()
            for website in website_list:
                if website in content:
                    pass
                else:
                    file.write(redirect + " " + website + "\n")
        print("Working time")
    else:
        with open(host_temp,'r+') as file:
            content=file.readlines()
            file.seek(0)
            for line in content:
                if not any(website in line for website in website_list):
                    file.write(line)
            file.truncate()
        print("Fun time!")
    time.sleep(5)