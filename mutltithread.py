#!/usr/bin/env python
import time
import urllib2
import HTMLParser
from BeautifulSoup import BeautifulSoup
import threading
import Queue

hosts = ["http://yahoo.com", "http://google.com", "http://amazon.com",
        "http://ibm.com", "http://apple.com","http://github.com"]


class Reader(threading.Thread):
    def __init__(self,queue):
        threading.Thread.__init__(self)
        self.queue  = queue
        self.setDaemon(True)
        
    def run(self):
        while 1:
            host = self.queue.get()
            read(host)
            self.queue.task_done()


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


def concuryRead():
    start = time.time()
    queue = Queue.Queue()
    [queue.put(host) for host in hosts]
    threads = [Reader(queue) for host in range(len(hosts)) ]
    [t.start() for t in threads]
    queue.join()
    end = time.time()
    print "Elapsed Time : %d" %(end-start)
    
if __name__ == '__main__':
    concuryRead()
