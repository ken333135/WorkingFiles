# -*- coding: utf-8 -*-
"""
Created on Fri Jan 26 08:53:44 2018

@author: jingwenken
"""

#this is so that we dont have to write tkiner.something
import sqlite3

def create_table():
    #creates a new db if none exists or connects to it if it already exitst
    conn=sqlite3.connect("lite.db")
    cur=conn.cursor()
    #SQL code goes in between the quotes
    cur.execute("CREATE TABLE IF NOT EXISTS store(item TEXT, quantity INT, price REAL)")
    #have to commit and close the connection
    conn.commit()
    conn.close
    
def insert(item,quantity,price):
    conn=sqlite3.connect("lite.db")
    cur=conn.cursor()
    cur.execute("INSERT INTO store VALUES (?,?,?)",(item,quantity,price))
    conn.commit()
    conn.close
    
def view():
    conn=sqlite3.connect("lite.db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM store")
    rows=cur.fetchall()
    conn.close()
    return rows

def delete(item):
    conn=sqlite3.connect("lite.db")
    cur=conn.cursor()
    cur.execute("DELETE FROM store WHERE item=?",(item,))
    conn.commit()
    conn.close()

def update(item,quantity,price):
    conn=sqlite3.connect("lite.db")
    cur=conn.cursor()
    cur.execute("UPDATE store SET quantity=?, price=? WHERE item=?",(quantity,price,item))
    conn.commit()
    conn.close()

print(view())
    