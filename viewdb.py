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
    
    if len(sys.argv)>3:
        table = sys.argv[1]
        sort = sys.argv[2]
        name = sys.argv[3]
        if len(sys.argv)>4:
            if name=='ALL':
                string = "SELECT * FROM "+table+" ORDER BY "+sort+" DESC"
            else:
                string = "SELECT * FROM "+table+" WHERE Name='"+name+"' ORDER BY "+sort+" DESC"
        else:
            if name=='ALL':
                string = "SELECT * FROM "+table+" ORDER BY "+sort+" ASC"
            else:
                string = "SELECT * FROM "+table+" WHERE Name='"+name+"' ORDER BY "+sort+" ASC"
    elif len(sys.argv)>2:
        table = sys.argv[1]
        sort = sys.argv[2]
        string = "SELECT * FROM "+table+"  ORDER BY "+sort+" ASC"
    else:
        print 'Usage: ./viewdb.py <table> <sort> <name>\n\t\t retrieve records from <table> and sort by <sort> for records with <name>'
        print '<table> Market, Stats, Node'
        print '<sort>\tMarket: Name, Date, Frame, Type, h1*h24'
        print '\tStats: Date, Expect, Min, Max, Dif, Neg'
        print '\tNode: Name, Frame, avgEx, avgMin, avgMax, avgDif, avgNeg'
        print '<name>\tex. MGE.MGE or ALL for all records'
        sys.exit(0)
        
    print string
    cur.execute(string)


    col_name_list = [tuple[0] for tuple in cur.description]
    rows = cur.fetchall()
    
    print col_name_list
    for row in rows:
        print row

