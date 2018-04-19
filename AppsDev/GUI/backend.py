# -*- coding: utf-8 -*-
"""
Created on Fri Jan 26 11:34:36 2018

@author: jingwenken
"""

import sqlite3

def create_table():
    conn=sqlite3.connect("library.db")
    cur=conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS books(id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, author TEXT, year INTEGER, ISBN INTEGER)")
    conn.commit()
    conn.close()

create_table()

def insert(title,author,year,ISBN):
    conn=sqlite3.connect("library.db")
    cur=conn.cursor()
    cur.execute("INSERT INTO books VALUES(NULL,?,?,?,?)",(title,author,year,ISBN))
    conn.commit()
    conn.close()
    
def delete(id):
    conn=sqlite3.connect("library.db")
    cur=conn.cursor()
    cur.execute("DELETE FROM books WHERE id=?",(id,))
    conn.commit()
    conn.close()

def search(title="",author="",year="",ISBN=""):
    conn=sqlite3.connect("library.db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM books WHERE title=? OR author=? or year=? or ISBN=?",(title,author,year,ISBN))
    rows=cur.fetchall()
    conn.commit()
    conn.close()
    return rows

def update(id,titlenew="",authornew="",yearnew="",ISBNnew=""):
    conn=sqlite3.connect("library.db")
    cur=conn.cursor()
    cur.execute("UPDATE books SET title=?, author=?, year=?, ISBN=? WHERE id=?",(titlenew,authornew,yearnew,ISBNnew,id))
    conn.commit()
    conn.close()


def view():
    conn=sqlite3.connect("library.db")
    cur=conn.cursor()
    cur.execute("SELECT * from books")
    rows=cur.fetchall()
    conn.close()
    return rows