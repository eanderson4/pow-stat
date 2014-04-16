#!/usr/bin/python


import sqlite3 as lite
import sys

con = None

con = lite.connect('power.db')

print sys.argv

with con:    
    cur = con.cursor()    
    cur.execute('SELECT SQLITE_VERSION()')
    data = cur.fetchone()
    print "SQLite version: %s" % data

    print "Create Node Database"
    cur.execute("DROP TABLE IF EXISTS Node")
    cur.execute("CREATE TABLE Node(Id INTEGER PRIMARY KEY, Name TEXT, Frame TEXT, avgEx REAL,avgVar REAL, avgMin REAL, avgMax REAL, avgDif, avgNeg)")
 
    table="Stats"   
    cur.execute("SELECT Name FROM "+table+" WHERE Date='2013-01-01' AND Frame='DA'")
    rows = cur.fetchall()
    
    names = [str(row[0]) for row in rows]
    print names

    for name in names:
        cur.execute("SELECT Name, Expect, Var, Min, Max, Dif, Neg FROM "+table+" WHERE Name='"+name+"' AND Frame='DA'")
        rows = cur.fetchall()
        n=0
        totalEx = 0        
        totalVar = 0
        totalMin = 0
        totalMax = 0
        totalDif = 0
        totalNeg = 0
        for row in rows:
            n=n+1
            totalEx = totalEx + row[1]
            totalVar = totalVar + row[2]
            totalMin = totalMin + row[3]
            totalMax = totalMax + row[4]
            totalDif = totalDif + row[5]
            totalNeg = totalNeg + row[6]
        exEx = totalEx/n
        exVar = totalVar/n
        exMin = totalMin/n
        exMax = totalMax/n
        exDif = totalDif/n
        exNeg = totalNeg/n
        cur.execute("INSERT INTO Node VALUES(NULL,'"+name+"', 'DA', "+str(exEx)+", "+str(exVar)+", "+str(exMin)+","+str(exMax)+","+str(exDif)+","+str(exNeg)+")")
        print name, exEx, exVar, exMin, exMax, exDif, exNeg

    cur.execute("SELECT * FROM Node")
    rows = cur.fetchall()
    for row in rows:
        print row
            

con.commit()

