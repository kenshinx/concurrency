#!/usr/bin/env python
import time
import urllib2
import HTMLParser
from BeautifulSoup import BeautifulSoup

hosts = ["http://yahoo.com", "http://google.com", "http://amazon.com",
        "http://ibm.com", "http://apple.com","http://github.com"]

def read(host):
    try:
        context = urllib2.urlopen(host,timeout=5)
    except urllib2.URLError:
        print "load %s failure." %host
        return
    try:
        title = BeautifulSoup(context).title.string
    except HTMLParser.HTMLParseError:
        print "paser %s tile failure" %host
    print "%s  : %s" %(host,title)
    

def singleRead():
    start = time.time()
    [read(host) for host in hosts]
    end = time.time()
    print "Elapsed Time : %d" %(end-start)
    
if __name__ == '__main__':
    singleRead()

