#!/usr/bin/env python

import time
import stackless
import urllib2
import HTMLParser
from BeautifulSoup import BeautifulSoup


"""
This script need stackless python 
"""

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
        return
    print "%s  : %s" %(host,title)
    

class Reader(object):
    def __init__(self,host):
        self.channel = channel
        stackless.tasklet(self.run)()
        
        
    def run(self):
        host = self.channel.receive()
        read(host)


def blockRead():
    start = time.time()
    channel = stackless.channel()
    [Reader(channel) for i in range(len(hosts))]
    [channel.send(host)  for host in hosts]
    stackless.run()
    end = time.time()
    
    print "Elapsed Time : %d" %(end-start)

if __name__ == '__main__':
    blockRead()


