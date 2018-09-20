#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys  
reload(sys)
sys.setdefaultencoding('utf_8')  

import csv, sqlite3

con = sqlite3.connect("NumberplateCodesManager.sqlite")

with open('jokes_for_v1.0.9.csv', 'rb') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=';', quotechar='|')
    for row in csvreader:
        print
        code = row[0].strip()
        joke = row[1].strip()
        print "Code: " + code
        print "Joke:     " + joke

        cur = con.cursor()    
        cur.execute("SELECT jokes FROM jokes WHERE code = '" + code + "'")
    
        db_rows = cur.fetchall()

        joke_already_in_db = False
 
        for db_row in db_rows:
            print "db entry: " + db_row[0] 
            if db_row[0] == joke:
                joke_already_in_db = True

        if joke_already_in_db:
            pass
            print "Joke already in database: " + joke
        else:
            print "Adding joke to database: " + joke
            cur.execute("SELECT MAX(_id)jokes FROM jokes")
            id_row = cur.fetchone()
            id = str(id_row[0] + 1)
            statement = "INSERT INTO jokes VALUES (" + id + ", " + "'" + code + "', '" + joke + "')"
            print statement
            cur.execute(statement)
            con.commit()

con.close()

