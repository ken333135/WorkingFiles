# -*- coding: utf-8 -*-
"""
Created on Fri Jan 26 08:53:44 2018

@author: jingwenken
"""

#this is so that we dont have to write tkiner.something
from tkinter import *

window=Tk()

def convertkg():
    grams = float(e1_value.get())*1000
    pounds = float(e1_value.get())*2.20462
    ounces = float(e1_value.get())*35.274
    t1.delete(1.0,END)
    t1.insert(END,grams)
    t2.delete(1.0,END)
    t2.insert(END,pounds)
    t3.delete(1.0,END)
    t3.insert(END,ounces)

b1=Button(window,text="Convert",command=convertkg)
b1.grid(row=0,column=2)

l1=Label(window,text="Kg")
l1.grid(row=0,column=0)

#for user input
e1_value=StringVar()
e1=Entry(window,textvariable=e1_value)
e1.grid(row=0,column=1)

t1=Text(window,height=1,width=15)
t1.grid(row=1,column=0)

t2=Text(window,height=1,width=15)
t2.grid(row=1,column=1)

t3=Text(window,height=1,width=15)
t3.grid(row=1,column=2)
window.mainloop()
