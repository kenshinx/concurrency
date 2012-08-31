#!/usr/bin/env python

import sys
import time
import socket
import errno
import urlparse
import StringIO
import HTMLParser
from BeautifulSoup import BeautifulSoup
from greenlet import greenlet
from greenlet import getcurrent


hosts = ["http://www.baidu.com", "http://www.amazon.com","http://www.ibm.com",
         "http://www.python.org","http://www.microsoft.com"]


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
        self.send_buffer = 'GET %s HTTP/1.0\r\n\r\n' % url
        self.out = StringIO.StringIO()
    
    def _connect(self):
        try:
            
            self.socket.connect(self.address)
        except socket.error,why:
            sys.stderr.write("CONNECT ERROR:%s\n" %why[0])
        self.socket.setblocking(0)
        Listener.register(self)
    
    @property       
    def recvable(self):
        return True
        
    def recv(self):
        try:
            data = self.socket.recv(128)
        except socket.error , why:
            data = why
        if isinstance(data,Exception):
            if why[0] not in [errno.WSAEWOULDBLOCK,errno.EAGAIN]:
                self.stop()
                sys.stderr.write("RECEIVE ERROR:%s\n" %why[0])
        elif data:
            self.out.write(data)
        else:
            self.stop()
        
    
    @property
    def sendable(self):
        return len(self.send_buffer)

    def send(self):
        try:
            sent = self.socket.send(self.send_buffer)
            self.send_buffer = self.send_buffer[sent:]
        except socket.error,why:
            if why[0] == errno.WSAEWOULDBLOCK:
                pass
            else:
                sys.stderr.write("SEND ERROR:%s\n" %why[0])
                self.stop()
    
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

    def __repr__(self):
        return "Reading %s" %self.url

def mainloop():
    while Listener._greenreaders:
        for gr in Listener._greenreaders:
            if gr.sendable:gr.send()
            if gr.recvable:gr.recv()
        print [Listener._greenreaders]
        time.sleep(0.01)


def concuryRead():
    start = time.time()
    grs = [GreenReader(host) for host in hosts]
    mainloop()
    print "xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    for gr in grs:
        context =  gr.out.getvalue()
        title = BeautifulSoup(context).title.string
        print "%s  : %s" %(gr.url,title)
        
    end = time.time()
    print "Elapsed Time : %d" %(end-start)


if __name__ == '__main__':
    concuryRead()