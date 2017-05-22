#coding: utf-8
import sqlite3
import urllib
import re
import ssl
from urlparse import urljoin
from urlparse import urlparse
from bs4 import BeautifulSoup
import time


scontext = None

conn = sqlite3.connect('spider.sqlite')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS Results
    (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, url TEXT UNIQUE, titre TEXT,
    prix TEXT, zone TEXT, cp TEXT, pieces TEXT,
    surface TEXT,chambre TEXT, metro1 TEXT, metro2 TEXT, metro3
    TEXT, tel TEXT, error INTEGER, cordN REAL, cordE REAL )''')
conn.commit()

starturl = raw_input('Enter a url to crawl')
sval = raw_input('How many pages:')
many = int(sval)
page=1
count = 0
url = None
while many>0:
    if page != 1:
        url = starturl+'-'+str(page)
    elif page == 1:
        url = starturl
    print 'Scaning:',url
    page+=1
    many = many - 1

    try:
        enter = urllib.urlopen(url)
        html = enter.read()
        if enter.getcode() != 200 :
            print "Error on page: ",enter.getcode()

        if 'text/html' != enter.info().gettype() :
            print "Ignore non text/html page"
            continue

        #print '('+str(len(html))+')',

        soup = BeautifulSoup(html,"lxml")
    except KeyboardInterrupt:
        print ''
        print 'Program interrupted by user...'
        break
    except:
        print "Unable to retrieve or parse page"
        continue

    tags = soup('a')
    href0 = list()#去重前的list

    for tag in tags:
        try:
            addr = 'http://www.pap.fr'+tag.get('href')
            addr = re.findall('^http.*/annonce/.*location.+r[0-9]+',addr)
            href0+=addr
        except:
            continue
    hrefs = list(set(href0)) #去重
    hrefs.sort(key = href0.index)

    for href in hrefs:
        try:
            cur.execute('INSERT OR IGNORE INTO Results (url) VALUES ( ? )', ( href, ) )
            count = count + 1
            print href
        except:continue
    conn.commit()
    if many>1:
        print "Waiting...."
        time.sleep(5)


print count,"urls have been retrieved!!"
cur.close()
