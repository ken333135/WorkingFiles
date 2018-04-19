# -*- coding: utf-8 -*-
"""
Created on Fri Jan 26 08:53:44 2018

@author: jingwenken
"""

#this is so that we dont have to write tkiner.something
import psycopg2

def create_table():
    #creates a new db if none exists or connects to it if it already exitst
    conn=psycopg2.connect("dbname='library' user='postgres' password='postgres123' host='localhost' port='5432'")
    cur=conn.cursor()
    #SQL code goes in between the quotes
    cur.execute("CREATE TABLE IF NOT EXISTS store(item TEXT, quantity INT, price REAL)")
    #have to commit and close the connection
    conn.commit()
    conn.close
    
def insert(item,quantity,price):
    conn=psycopg2.connect("dbname='library' user='postgres' password='postgres123' host='localhost' port='5432'")
    cur=conn.cursor()
    #the first one is prone to SQL attacks
    #cur.execute("INSERT INTO store VALUES ('%s','%s','%s')" & (item,quantity,price))
    cur.execute("INSERT INTO store VALUES (%s,%s,%s)",(item,quantity,price))
    conn.commit()
    conn.close
    
def view():
    conn=psycopg2.connect("dbname='library' user='postgres' password='postgres123' host='localhost' port='5432'")
    cur=conn.cursor()
    cur.execute("SELECT * FROM store")
    rows=cur.fetchall()
    conn.close()
    return rows

def delete(item):
    conn=psycopg2.connect("dbname='library' user='postgres' password='postgres123' host='localhost' port='5432'")
    cur=conn.cursor()
    cur.execute("DELETE FROM store WHERE item=%s",(item,))
    conn.commit()
    conn.close()

def update(item,quantity,price):
    conn=psycopg2.connect("dbname='library' user='postgres' password='postgres123' host='localhost' port='5432'")
    cur=conn.cursor()
    cur.execute("UPDATE store SET quantity=%s, price=%s WHERE item=%s",(quantity,price,item))
    conn.commit()
    conn.close()