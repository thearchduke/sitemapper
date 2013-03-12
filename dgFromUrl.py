import requests
from bs4 import BeautifulSoup as bs
from urlparse import urljoin

import Queue
import threading

import networkx as nx
import pylab as plt

import json, sys

########### POSSIBLE IDEA FOR INDEPENDENT STUDY
###### Will eventually involve networkx &c. for visualization
###### Can be more universal than existing tools b/c a Flask app can run this (therefore the internet can do
######   it for arbitrary machines)
########### TO DO:
###### Research existing tools better
###### Plug everything into a graph for visualization
###### Learn how said graphs work



masterKeys = []

def getLinks(url, domain):
    linked = {url:[]}

    soup = bs(requests.get(url).text)

    for link in soup.find_all('a'):
        testLocal = urljoin(url, link.get('href'))
        if domain in testLocal \
            and '.pdf' not in testLocal \
            and '.PDF' not in testLocal \
            and '.flv' not in testLocal \
            and '.jpg' not in testLocal \
            and '.mp' not in testLocal \
            and 'mailto:' not in testLocal \
            and '.png' not in testLocal:
            if '#' in testLocal:
                removeHash = testLocal.split('#')[0]
                linked[url].append(removeHash)
                #masterKeys.append(url)
                #print url + ' links to ' + removeHash
            else:
                linked[url].append(testLocal)
                #masterKeys.append(url)
                #print url + ' links to ' + testLocal
    return linked


#### See above comment. But basically, this reads the list it returns. Good for recursion.
#### Going to need to transfer this to a dictionary so we can support uniqueness and direction of links.
#### Gonna need some whiteboard time here. Maybe talk to Alan about this??
def readList(urlList, domain):
    out = []
    for url in urlList:
        if url not in masterKeys:
            print 'appending ' + url
            tempOut = getLinks(url, domain)
            out.append(tempOut)
            masterKeys.append(url)
    #print 'out: '
    #print out
    return out

fullURL = str(sys.argv[1]) # Note that DNS issues complicate the inclusion of www., &c here
domainBase = fullURL.split('://')[1]
deep = int(sys.argv[2])

starter = getLinks(fullURL, domainBase)

out = readList(starter[fullURL], domainBase)

#### depth = 2
i = 1
out2 = []
out2 = out[:]
out3 = []
out3 = out2[:]

print "Starting with:"
print out2

import sys

while i <= deep:
    print 'recursing'
    for d in out2:
        #print 'recursing on'
        #print out2
        for k in d:
            print 'new list'
            #print d
            #print "^^^What's the problem?"
            test = readList(d[k], domainBase)
            try:
                out3.append(test[0])
            except:
                print "empty set, moving on"
    out2 = []
    out2 = out3[:]
    i += 1

fout = open('testOut.json', 'w')
fout.write(json.dumps(out3))
fout.close()



##############################################
#### DRAWING PORTION
############################
#
#
#

print "DRAWING..."

import networkx as nx
import pylab as plt
import json

import hashlib

h = nx.MultiDiGraph()

fin = open('testOut.json')
jsonData = fin.read()
siteMap = json.loads(jsonData)


### for arbitrary(?) depth:
e_colors = []
for page in siteMap:
    for key in page:
        tempColor = '#' + str(int(hashlib.md5(key).hexdigest(), 16))[0:6]
        for url in page[key]:
            h.add_edge(key, url)
            e_colors.append(tempColor)

#print e_colors

plt.figure(1, figsize=(55,55))

pos=nx.spring_layout(h)

nx.draw_networkx_nodes(h,pos,node_size=200)

nx.draw_networkx_edges(h,pos,width=1,data=True,edge_color=e_colors)

nx.draw_networkx_labels(h,pos,font_size=10,font_family='sans-serif', font_color='#112233')

plt.axis('off')
plt.savefig('graph.png')
#plt.show()
