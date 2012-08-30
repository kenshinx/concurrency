#!/usr/bin/env python

import time
import socket
import sys
import urlparse
import StringIO
import HTMLParser
from BeautifulSoup import BeautifulSoup
from greenlet import greenlet
from greenlet import getcurrent


hosts = ["http://www.yahoo.com", "http://www.baidu.com", "http://www.amazon.com",
        "http://www.ibm.com", "http://www.python.org","http://www.microsoft.com"]


class Listener(object):
    
    _greenreaders = []

    @classmethod
    def register(cls,reader):
        cls._greenreaders.append(reader)
    
    @classmethod
    def unregister(cls,reader):
        cls._greenreaders.remove(reader)
        
        
class GreenReader(object):
    
    def __init__(self,url):
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.url = url
        host = urlparse.urlparse(url).netloc
        self.address = (host,80)
        self._connect()
        self.terminate = False
        self.write_buffer = 'GET %s HTTP/1.0\r\n\r\n' % url
        self.out = StringIO.StringIO()
    
    def _connect(self):
        self.socket.settimeout(5)
        self.socket.setblocking(0)
        try:
            self.socket.connect(self.address)
        except socket.error,why:
            sys.stderr.write("CONNECT ERROR:%s\n" %why[0])
            print why   
        Listener.register(self)
    
    @property       
    def readable(self):
        return True
        
    def read(self):
        try:
            data = self.socket.recv(128)
        except socket.error as e:
            sys.stderr.write("RECEIVE ERROR:%s\n" %e[0])
            data = e
        if isinstance(data,Exception):
            self.stop()
        elif data:
            self.out.write(data)
        else:
            self.stop()
        
    
    @property
    def writeable(self):
        return len(self.write_buffer)

    def write(self):
        print self.write_buffer
        sent = self.socket.send(self.write_buffer)
        self.write_buffer = self.write_buffer[sent:]
    
    def __loop__(self):
        pass

    def stop(self):
        self.terminate = True
        Listener.unregister(self)
        self._close()
    
    def _close(self):
        try:
            self.socket.close()
        except socket.error,why:
            sys.stderr.write("CLOSE ERROR:%s\n" %why[0])

def mainloop():
    while Listener._greenreaders:
        for gr in Listener._greenreaders:
            if gr.writeable:gr.write()
            if gr.readable:gr.read()
            time.sleep(0.01)


def concuryRead():
    start = time.time()
    grs = [GreenReader(host) for host in hosts]
    mainloop()
    for gr in grs:
        context =  gr.out.getvalue()
        title = BeautifulSoup(context).title.string
        print "%s  : %s" %(gr.url,title)
        
    end = time.time()
    print "Elapsed Time : %d" %(end-start)


if __name__ == '__main__':
    concuryRead()