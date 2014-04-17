#!/usr/bin/python

import sqlite3 as lite
import sys

con = None

con = lite.connect('power.db')

cur = con.cursor()

hours = ""
for i in range(24):
    hours =hours+", h"+str(i+1)

daysinmonth=[31,28,31,30,31,30,31,31,30,31,30,31]
leapyear=[2008,2012]
daysinleap=[31,29,31,30,31,30,31,31,30,31,30,31]

if len(sys.argv)>2:
    print sys.argv
    filename = sys.argv[1]
    dataframe = sys.argv[2]
else:
    print "Usage: ./filldb.py <filename> <frame>   \t\t where <frame> = DA or RT"
    sys.exit(0)

class Data:
    def __init__(self,datatype,date,prices):
        self.datatype=datatype
        self.date=date
        self.prices=prices

class Node:
    def __init__(self,name,bus,ty):
        self.name=name
        self.bus=bus
        self.nodetype=ty
        self.dataLMP = { '0/0/0000':Data('none','0/0/0000',[0]) }
        self.dataMCC = { '0/0/0000':Data('none','0/0/0000',[0]) }
        self.dataMLC = { '0/0/0000':Data('none','0/0/0000',[0]) }

    def addLMP(self,data):
#        self.dataLMP[data.date] = data
        string = "NULL, '"+str(self.name)+"', '"+self.bus+"', '"+dataframe+"', 'LMP',"
        string2 = "NULL, '"+str(self.name)+"', '"+dataframe+"', 'LMP',"
        ds = data.date.split('/')[2].rstrip() + '-' 
        year = data.date.split('/')[2].rstrip()
        if len(data.date.split('/')[0])>1:
            ds = ds + data.date.split('/')[0] +'-'
            month=data.date.split('/')[0]
        else:
            ds = ds + '0'+data.date.split('/')[0] +'-'
            month='0' + data.date.split('/')[0]
        if len(data.date.split('/')[1])>1:
            ds = ds + data.date.split('/')[1]
            day = data.date.split('/')[1]
        else:
            ds = ds + '0'+data.date.split('/')[1]
            day = '0' + data.date.split('/')[1]
        date=year+'-'+month+'-'+day
#        print year,month,day,'-',ds
        string = string + " '"+ ds+"'" 
        stringstat = string
        stringstat2 = string2+ " '"+ ds+"'" 
        for p in data.prices:
            string = string + ", "+str(p)
#        print data.date, data.prices
#        print string

        cur.execute("INSERT INTO Market VALUES("+string+")")


        tempdays=0
        for i in range(int(month)-1):
            if int(year) in leapyear:
                tempdays=tempdays+daysinleap[i]
            else:
                tempdays=tempdays+daysinmonth[i]
        tempdays=tempdays+int(day)
#        print tempdays,data.prices
        hour = (int(tempdays)-1)*24
        for p in data.prices:
            hour=hour+1
#            print hour,p
            string="'"+date+"', '"+str(self.name)+"', "+str(year)+", "+str(tempdays)+", "+str(hour)+", "+str(p)
#            print string
#            cur.execute("INSERT INTO Pricedata VALUES("+string+")")


        ps = data.prices
        
        total = 0
        n = 0
        mn = 1000
        mx = 0
        neg = 0
        for p in ps:
            n = n+1
            value = float(p)
            total = total + value
            if value < 0:
                neg = neg - value
            if value < mn:
                mn = value
            if value > mx:
                mx = value
        ex = total/n

        t2 = 0
        for p in ps:
            value = float(p)
            t2 = t2 + (value - ex)**2
            s2 = t2/(n-1)

#        print data.date, mn, mx, (mx-mn), ex, s2
        stringstat2 = stringstat2+", "+str(ex)+", "+str(s2)+", "+str(mn)+", "+str(mx)+", "+str(mx-mn)+", "+str(neg)
        cur.execute("INSERT INTO Stats VALUES("+stringstat2+")")

    def addMCC(self,data):
        self.dataMCC[data.date] = data
    def addMLC(self,data):
        self.dataMLC[data.date] = data
        

f = open(filename,'r')

n = Node('blank','none','none')
nodelist = { n.name:n }

for example in f:
    example = example[:-2]    
    date=example.split(',')[0]
#    if date=='1/5/2013':
#        break
    name=example.split(',')[1]
    bus=example.split(',')[2]
    nodetype=example.split(',')[3]

    if name not in nodelist.keys():
        nodelist[name] = Node(name,bus,nodetype)
#        print name,',',

    if 'LMP' in example and 'MCC' not in example and 'MLC' not in example:
        p = example.split(',LMP,')
        d = Data('LMP',date,p[1].split(','))
        nodelist[name].addLMP(d)
    elif 'MCC' in example and 'MLC' not in example and 'LMP' not in example:    
        p = example.split(',MCC,')
        d = Data('MCC',date,p[1].split(','))
        nodelist[name].addMCC(d)
    elif 'MLC' in example:    
        p = example.split(',MLC,')        
        d = Data('MLC',date,p[1].split(','))
        nodelist[name].addMLC(d)


con.commit()

