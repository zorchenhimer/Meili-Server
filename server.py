#!/usr/bin/python

#from multiprocessing import Process
from Lib.HTTPInterface import HTTPThread

if __name__ == '__main__':
	http = HTTPThread()
	http.start()
	http.join()