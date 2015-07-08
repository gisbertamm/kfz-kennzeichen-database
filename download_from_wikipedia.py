#!/usr/bin/python

import urllib2
from bs4 import BeautifulSoup
from proxy_url import proxy_url

print "Configuring Proxy..."
proxy = urllib2.ProxyHandler({'https': proxy_url})
auth = urllib2.HTTPBasicAuthHandler()
opener = urllib2.build_opener(proxy, auth, urllib2.HTTPHandler)
urllib2.install_opener(opener)

response = urllib2.urlopen('https://de.wikipedia.org/wiki/Liste_der_Kfz-Kennzeichen_in_Deutschland')
print "Downloading Kfz-Kennzeichen in Deutschland..."
html = response.read()

print "Parsing Kfz-Kennzeichen in Deutschland..."
soup = BeautifulSoup(html, 'html.parser')
result = []
row_should_be_cloned = False

for table in soup.find_all('table'):
    if table.tr.th.get_text() == 'Abk.':
        for row in table.find_all('tr'):
            if row_should_be_cloned:
                row_should_be_cloned = False
                row_result = result[-1]
                td_list = row.find_all('td')
                for cell in td_list:
                    # overwrite existing values - only the second cell differs
                    if cell.get_text():
                        row_result[1] = cell.get_text()
            else:
                row_result = []
                for cell in row.find_all('td'):
                    if cell.get('rowspan') == '2' and cell.parent.name == 'tr':
                        # clone row later
                        row_should_be_cloned = True
                    row_result.append(cell.get_text())
                if len(row_result) > 0:
                    result.append(row_result)
                    if row_should_be_cloned:
                        clone = []
                        for elem in row_result:
                            clone.append(elem)
                        result.append(clone)

for row in result:
    print row
