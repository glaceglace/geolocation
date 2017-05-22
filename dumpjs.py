#coding: utf-8
import sqlite3
import json
import codecs
import sys

conn = sqlite3.connect('spider.sqlite')
cur = conn.cursor()

cur.execute('SELECT * FROM Results')
fhand = codecs.open('locations.js','w', 'utf-8')
fhand.write("myLocations = [\n")
count = 0
for row in cur :
    lat = str(row[14])
    lng = str(row[15])
    if lat == 'NULL' or lat == 'NULL':continue
    url = row[1]
    title = row[2]
    title =  unicode(title).replace("'","\\'")
    price = row[3]
    zone = row[4]
    cp = row[5]
    pieces = row[6]
    surface = row[7]
    chambre = row[8]
    metro1 = row[9]
    metro1 = unicode(metro1).replace("'","\\'")
    metro2 = row[10]
    metro2 = unicode(metro2).replace("'","\\'")
    metro3 = row[11]
    metro3 = unicode(metro3).replace("'","\\'")
    tel = row[12]
    try :
        count = count + 1
        if count > 1 : fhand.write(",\n")
        output = "["+lat+","+lng+", '"+url+"\', \'"+title+"\', \'"+price+"\', \'"+zone+"\', \'"+cp+"\', \'"+pieces+"\', \'"+surface+"\', \'"+chambre+"\', \'"+metro1+"\', \'"+metro2+"\', \'"+metro2+"\', \'"+metro3+"\', \'"+tel+"']"
        fhand.write(output)
    except:
        print sys.exc_info,sys.exc_type
        continue

fhand.write("\n];\n")
cur.close()
fhand.close()
print count, "records written to locations.js"
print "Open map.html to view the data in a browser"
