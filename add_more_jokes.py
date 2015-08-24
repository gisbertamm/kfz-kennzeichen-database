#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys  
reload(sys)
sys.setdefaultencoding('utf_8')  

import csv, sqlite3

con = sqlite3.connect("NumberplateCodesManager.sqlite")

with open('more_jokes.csv', 'rb') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=';', quotechar='|')
    for row in csvreader:
        print "Code: " + row[0]

        cur = con.cursor()    
        cur.execute("SELECT jokes FROM jokes WHERE code = '" + row[0] + "'")
    
        db_rows = cur.fetchall()
 
        for db_row in db_rows:
            print "Checking against DB: " + db_row[0] 
            if db_row[0] == row[1]:
                print "Joke already in database " + row[1]
            else:
                print "Adding joke to database " + row[1]

con.close()
