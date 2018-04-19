# -*- coding: utf-8 -*-
"""
Created on Fri Jan 26 11:15:36 2018

@author: jingwenken
"""

from tkinter import *
import backend
#building the GUI

window=Tk()

title_label=Label(window,text="Title")
title_label.grid(row=0,column=0)
author_label=Label(window,text="Author")
author_label.grid(row=0,column=2)
year_label=Label(window,text="Year")
year_label.grid(row=1,column=0)
ISBN_label=Label(window,text="ISBN")
ISBN_label.grid(row=1,column=2)

title_text=StringVar()
title_entry=Entry(window,textvariable=title_text)
title_entry.grid(row=0,column=1)

author_text=StringVar()
author_entry=Entry(window,textvariable=author_text)
author_entry.grid(row=0,column=3)

year_text=StringVar()
year_entry=Entry(window,textvariable=year_text)
year_entry.grid(row=1,column=1)

ISBN_text=StringVar()
ISBN_entry=Entry(window,textvariable=ISBN_text)
ISBN_entry.grid(row=1,column=3)

list1=Listbox(window,height=6,width=35)
list1.grid(row=2,column=0,rowspan=6,columnspan=2)

sb1=Scrollbar(window)
sb1.grid(row=2,column=2,rowspan=6)
#to link the scrollbar and the list
list1.configure(yscrollcommand=sb1.set)
sb1.configure(command=list1.yview)

view_button=Button(window,text="View All",width=12)
view_button.grid(row=2,column=3)
search_button=Button(window,text="Search Entry",width=12)
search_button.grid(row=3,column=3)
add_button=Button(window,text="Add Entry",width=12)
add_button.grid(row=4,column=3)
update_button=Button(window,text="Update entry",width=12)
update_button.grid(row=5,column=3)
delete_button=Button(window,text="Delete",width=12)
delete_button.grid(row=6,column=3)
close_button=Button(window,text="Close",width=12)
close_button.grid(row=7,column=3)



window.mainloop()