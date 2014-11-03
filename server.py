#!/usr/bin/python

#from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
#from Lib.API import BaseAPIHandler
from Lib.HTTPInterface import HTTPThread

http = HTTPThread()
http.run()
