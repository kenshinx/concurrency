#!/usr/bin/env python

import time
import stackless
import urllib2
import HTMLParser
from BeautifulSoup import BeautifulSoup


"""
This is a negative concurrence example. 
run need stackless python.
"""

hosts = ["http://www.yahoo.com", "http://www.baidu.com", "http://www.amazon.com",
        "http://www.ibm.com", "http://www.python.org","http://www.microsoft.com"]
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
    def __init__(self,channel):
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


