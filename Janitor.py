#!/usr/bin/python

from multiprocessing import Process, Queue, freeze_support
import queue
import time
from Lib.Database import SQLiteDB
import sys, signal

def Loop(q):
    print('Starting janitor.')
    db = SQLiteDB()
    running = True
    while running:
        print('ping')
        db.update_delayed()
        db.clear_canceled()
        db.clear_done()
        time.sleep(5)

        r = None
        try:
            r = q.get_nowait()
        except queue.Empty:
            # Ignore an empty queue
            pass

        if r is True:
            running = False
            print('Janitor stopping...')
    print('Stopped.')

def handler(signal, frame):
    print('Frame: {f}'.format(f=frame))
    print('Stopping...')
    procQueue.put(True)
    proc.join()
    sys.exit(0)

procQueue = Queue()
proc = Process(target=Loop, args=(procQueue,))
signal.signal(signal.SIGINT, handler)

if __name__ == '__main__':
    freeze_support()
    proc.start()
    while 1:
        print('pong')
        time.sleep(5)
        pass

