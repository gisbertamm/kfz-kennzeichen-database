#!/usr/bin/python
# encoding=utf8

import urllib2, sqlite3
from bs4 import BeautifulSoup
from proxy_url import proxy_url
import sys, os
reload(sys)
sys.setdefaultencoding('utf8')

print "Configuring Proxy..."
proxy = urllib2.ProxyHandler({'https': proxy_url})
auth = urllib2.HTTPBasicAuthHandler()
opener = urllib2.build_opener(proxy, auth, urllib2.HTTPHandler)
urllib2.install_opener(opener)

wiki_base_url = "https://de.wikipedia.org"
script_dir = os.path.dirname(__file__) #<-- absolute dir this script is in
replacement_dict = {'ä':'ae', 'ö':'oe', 'ü':'ue'}

con = None

try:
    con = sqlite3.connect("NumberplateCodesManager.sqlite")

    cur = con.cursor()
    cur.execute("SELECT code, district_wikipedia_url FROM numberplate_codes")

    data = cur.fetchall()

    for entry in data:
        print "Code: " + entry[0]
        if entry[1] != "-":
            url = wiki_base_url + entry[1]
            print "Downloading " + url + " ..."
            response = urllib2.urlopen(url)
            html = response.read()

            print "Parsing site for " + entry[1] + " ..."
            soup = BeautifulSoup(html, 'html.parser')

            #save all image urls
            image_urls = {}
            for img in soup.find_all('img'):
                if img.get('alt'):
                    if img.get('alt').startswith("Wappen"):
                        image_urls[int(img.get('width'))] = "https:" + img.get('src')

            if image_urls: # dict is not empty
                # pick only biggest size
                image_url = image_urls[max(image_urls.keys())]
                print "Downloading image " + image_url + " ..."
                img_response = urllib2.urlopen(image_url)
                filename = entry[0].lower() + ".png"
                for key in replacement_dict:
                    filename = filename.replace(key, replacement_dict[key])
                path = os.path.join(script_dir, "./crests/" + filename)
                if os.path.exists(path):
                    print "File exists: " + path
                else:
                    print "Writing " + path + " ..."
                    fh = open(path,'wb')
                    fh.write(img_response.read())
                    fh.close()
            else:
                print "TODO dict is empty"

except sqlite3.Error, e:

    print "Error %s:" % e.args[0]
    sys.exit(1)

finally:

    if con:
        con.close()
