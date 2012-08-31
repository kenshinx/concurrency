#!/usr/bin/env python

import time
import asyncore
import urlparse
import socket
import StringIO
import HTMLParser
from BeautifulSoup import BeautifulSoup


hosts = ["http://www.baidu.com", "http://www.amazon.com","http://www.ibm.com",
         "http://www.python.org","http://www.microsoft.com"]


class AsyncRead(asyncore.dispatcher):
    
    def __init__(self,url):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.out = StringIO.StringIO()
        self.url = url
        self.host = urlparse.urlparse(self.url).netloc
        self.write_buffer = 'GET %s HTTP/1.0\r\n\r\n' % self.url
        self.connect((self.host,80))
        
    
    def handle_connect(self):
        pass
    
    def writable(self):
        return len(self.write_buffer)
    
    def handle_write(self):
        sent = self.send(self.write_buffer)
        self.write_buffer = self.write_buffer[sent:]
    
    def handle_read(self):
        context =  self.recv(1024)
        self.out.write(context)
        
   

def unblockRead():
    start = time.time()
    readers = [AsyncRead(host) for host in hosts]
    asyncore.loop(timeout=5)
    for reader in readers:
        context =  reader.out.getvalue()
        title = BeautifulSoup(context).title.string
        print "%s  : %s" %(reader.url,title)
        
    end = time.time()
    
    print "Elapsed Time : %d" %(end-start)
    

if __name__ == '__main__':
    unblockRead()