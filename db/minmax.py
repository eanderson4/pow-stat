#!/usr/bin/python

import sys
print 'Day,Price'
for line in sys.stdin.readlines():
    date=line.split(' ')[0]
    numbers=[float(i) for i in line.split(' ')[1:]]

    print date+','+str(min(numbers))+';'+str(sum(numbers)/len(numbers))+';'+str(max(numbers))
