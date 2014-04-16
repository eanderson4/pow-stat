#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys

con = None

con = lite.connect('power.db')


with con:    
    cur = con.cursor()    
    cur.execute('SELECT SQLITE_VERSION()')
    data = cur.fetchone()
    print "SQLite version: %s" % data
    print "Create Market and Stats database"

    hours = ""
    for i in range(24):
        hours =hours+", h"+str(i+1)+" REAL"

    
    cur.execute("DROP TABLE IF EXISTS Market")
    cur.execute("CREATE TABLE Market(Id INTEGER PRIMARY KEY, Name TEXT, Frame TEXT, Type TEXT, Date DATE"+hours+")")

    cur.execute("DROP TABLE IF EXISTS Stats")
    cur.execute("CREATE TABLE Stats(Id INTEGER PRIMARY KEY, Name TEXT, Frame TEXT, Type TEXT, Date Date, Expect REAL, Var REAL, Min REAL, Max REAL, Dif REAL, Neg REAL)")

    cur.execute("DROP TABLE IF EXISTS Pricedata")
    cur.execute("CREATE TABLE Pricedata(Date DATE, Name TEXT, Year INTEGER, Day INTEGER, Hour INTEGER, Price REAL)")

    cur.execute("SELECT * FROM Market")
    rows = cur.fetchall()
    
    for row in rows:
        print str(row[1])
