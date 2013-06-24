concurrency
===================

Concurrency http request client .implement by different python library.

include:

`multi-thread`,`multiprocess`,`stackless`,`async`,`greent`,`gevent`


The benchmark of different program version.

singethread.py  :   252s

multithread.py  :   17s

multiprocess.py :   40s

blockstackless.py   :   240s

async.py    :   13s

_greenlet.py    :   6s

_gevent.py  :   6s

*Supplement go-goroutine implement.*

goroutine.go : 4.6s


[!!] Note: The bechmark result is just for learning. Nerver consider it in your production.




