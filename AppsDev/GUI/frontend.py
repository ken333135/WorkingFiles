# -*- coding: utf-8 -*-
"""
Created on Fri Jan 26 11:15:36 2018

@author: jingwenken
"""
from tkinter import *
import backend
#building the GUI

#grabs the output from view an puts them into the ListBox
def view_command():
    list1.delete(0,END)
    for row in backend.view():
        list1.insert(END,row)

def search_command():
    list1.delete(0,END)
    for row in backend.search(title_text.get(),author_text.get(),year_text.get(),ISBN_text.get()):
        list1.insert(END,row)

def insert_command():
    list1.delete(0,END)
    backend.insert(title_text.get(),author_text.get(),year_text.get(),ISBN_text.get())
    for row in backend.search(title_text.get(),author_text.get(),year_text.get(),ISBN_text.get()):
        list1.insert(END,row)

#special parameter called event as it is bound to an event function below (.bind)
def get_selected_row(event):
    try:
        global selected_tuple
        index=list1.curselection()[0]
        selected_tuple=list1.get(index)
        title_entry.delete(0,END)
        title_entry.insert(END,selected_tuple[1])
        author_entry.delete(0,END)
        author_entry.insert(END,selected_tuple[2])
        year_entry.delete(0,END)
        year_entry.insert(END,selected_tuple[3])
        ISBN_entry.delete(0,END)
        ISBN_entry.insert(END,selected_tuple[4])
    except IndexError:
        pass

def delete_command():
    backend.delete(selected_tuple[0])
    view_command()

def update_command():
    backend.update(selected_tuple[0],title_text.get(),author_text.get(),year_text.get(),ISBN_text.get())
    view_command()

window=Tk()
window.wm_title("BookStore")


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
list1.bind('<<ListboxSelect>>',get_selected_row)

view_button=Button(window,text="View All",width=12,command=view_command)
view_button.grid(row=2,column=3)
search_button=Button(window,text="Search Entry",width=12,command=search_command)
search_button.grid(row=3,column=3)
add_button=Button(window,text="Add Entry",width=12,command=insert_command)
add_button.grid(row=4,column=3)
update_button=Button(window,text="Update entry",width=12,command=update_command)
update_button.grid(row=5,column=3)
delete_button=Button(window,text="Delete",width=12,command=delete_command)
delete_button.grid(row=6,column=3)
close_button=Button(window,text="Close",width=12,command=window.destroy)
close_button.grid(row=7,column=3)

window.mainloop()