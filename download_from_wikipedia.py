#!/usr/bin/python
# encoding=utf8

import urllib2
from bs4 import BeautifulSoup
from proxy_url import proxy_url
import sys
reload(sys)
sys.setdefaultencoding('utf8')

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
row_should_be_cloned = 0

for table in soup.find_all('table'):
    if table.tr.th.get_text() == 'Abk.':
        for row in table.find_all('tr'):
            if row_should_be_cloned > 0:
                # create clone
                row_result = result[-1]
                clone = []
                for elem in row_result:
                    clone.append(elem)
                result.append(clone)

                # change clone
                for cell in row.find_all('td'):
                    # overwrite existing values - only the second cell differs
                    if cell.get_text():
                        clone[1] = cell.get_text()
                row_should_be_cloned -= 1
            else:
                row_result = []
                for cell in row.find_all('td'):
                    rowspan = 1
                    if cell.get('rowspan'):
                        rowspan = int(cell.get('rowspan'))
                    if rowspan > 1 and cell.parent.name == 'tr':
                        # clone row later to match the number of lines in rowspan
                        row_should_be_cloned = rowspan - 1
                    row_result.append(cell.get_text())
                if len(row_result) > 0:
                    result.append(row_result)

print "Writing dataset.xml..."

dataset = """<!DOCTYPE dataset SYSTEM "dataset.dtd">
<dataset>
    <table name="numberplate_codes">
        <column>id</column>
        <column>code</column>
        <column>district</column>
        <column>district_center</column>
        <column>state</column>
        <column>district_wikipedia_url</column>
        <column>jokes</column>"""

row_template = """
        <row>
            <value>%(id)s</value>
            <value>%(code)s</value>
            <value>%(district)s</value>
            <value>%(district_center)s</value>
            <value>%(state)s</value>
            <value>%(district_wikipedia_url)s</value>
            <value>%(jokes)s</value>
        </row>"""

# prepare the data and add them to the dataset
id = 0
for row in result:
    if len(row) == 2: 
        row_dict = {'id':id, 'code':row[0], 'district':row[1], 'district_center':'-', 'state':'-', 'district_wikipedia_url':'TODO', 'jokes':'TODO'}
    if len(row) == 4: 
        row_dict = {'id':id, 'code':row[0], 'district':row[1], 'district_center':row[2], 'state':row[3], 'district_wikipedia_url':'TODO', 'jokes':'TODO'}
    dataset += row_template%row_dict
    id += 1

# close XML
dataset += """
</dataset>"""

# write dataset to file
f = open('dataset.xml','w')
f.write(dataset)
f.close()
