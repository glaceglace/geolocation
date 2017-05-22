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
conn.text_factory = str
cur = conn.cursor()
urls = list()
many = 0
result=dict()
num=0
cur.execute('''SELECT url FROM Results''')
for row in cur:
    urls.append(str(row[0]))

for url in urls:
    print url
    metro1 = 'NULL'
    metro2 = 'NULL'
    metro3 = 'NULL'
    try:
        enter = urllib.urlopen(url)
        html = enter.read()
        if enter.getcode() != 200 :
            print "Error on page: ",enter.getcode()
            cur.execute('UPDATE Results SET error=? WHERE url=?', (enter.getcode(), url) )
        if 'text/html' != enter.info().gettype() :
            print "Ignore non text/html page"
            cur.execute('UPDATE Results SET error=? WHERE url=?', (enter.info().gettype(), url) )
            continue
        soup = BeautifulSoup(html,'lxml')
    except KeyboardInterrupt:
        print ''
        print 'Program interrupted by user...'
        break
    except:
        print "Unable to retrieve or parse page"
        cur.execute('UPDATE Results SET error=-1 WHERE url=?', (url, ) )
        conn.commit()
        continue
    print 'converting'
    tags = soup('span')
    for tag in tags:
        father = tag.parent
        try:
            if tag['class']==['title'] and father['class']==['clearfix']:
                title = tag.string
            elif tag['class']==['price']:
                price = tag.string
            elif tag['class'] == ['label'] and father.parent['class']==['item-metro'] and father.parent.parent['class']==['box-body']:
                if metro1 == 'NULL':
                    metro1=tag.string
                elif metro2 == 'NULL':
                    metro2=tag.string
                elif metro3 == 'NULL':
                    metro3=tag.string
                else: continue
            else:
                continue
        except:
            #print tag,sys.exc_info,sys.exc_type
            continue
    try:result['pieces'] = re.findall('Pi.+<strong>([0-9]+)</strong',html)[0]
    except:result['piece'] = 'NULL'
    try:result['chambre'] = re.findall('Ch.+<strong>([0-9]+)</strong',html)[0]
    except:result['chambre'] = 'NULL'
    try:result['surface'] = unicode((re.findall('Su.+<strong>([0-9]+).*</strong',html))[0])
    except:result['surface'] = 'NULL'
    try:result['cordN'] = float((re.findall('data-mappy.+([0-9][0-9]\\.[0-9]+).+[0-9]+\\.[0-9+]',html))[0])
    except:result['cordN'] = 'NULL'
    try:result['cordE'] = float((re.findall('data-mappy.+[0-9][0-9]\\.[0-9]+.+([0-9]+\\.[0-9]+)',html))[0])
    except:result['cordE'] = 'NULL'
    try:result['zone'] = unicode(re.findall('h2>(.+)\s\\([0-9]+.<',html)[0])
    except:result['zone'] = 'NULL'
    try:result['cp'] = re.findall('h2>.+\s\\(([0-9]+).<',html)[0]
    except:result['cp'] = 'NULL'
    try:result['tel'] = re.findall('tel-wrapper.+>(.+)<br',html)[0]
    except:result['tel'] = 'NULL'
    result['title'] = unicode(title)
    result['price'] = price
    result['metro1'] = unicode(metro1)
    result['metro2'] = unicode(metro2)
    result['metro3'] = unicode(metro3)

    cur.execute('''UPDATE Results SET (pieces,chambre,surface,cordN,cordE,zone,cp,tel,titre,prix,metro1,metro2,metro3)=(?,?,?,?,?,?,?,?,?,?,?,?,?) WHERE url=?''', (result['pieces'],result['chambre'],result['surface'],result['cordN'],result['cordE'],result['zone'],result['cp'],result['tel'],result['title'],result['price'],result['metro1'],result["metro2"], result['metro3'], url,))
print 'Complete!!!'
conn.commit()
cur.close()
