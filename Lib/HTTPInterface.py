#!/usr/bin/python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from multiprocessing import Process
from API import *
import urllib
#import signal

__all__ = "HTTPThread".split(' ')

def parse_urivars(varstring):
	## varstring is the uri minus everything before, and including, the '?'.
	print 'parsing varstring: %s' % str(varstring)
	retdict = {}
	urivars = varstring.split('&')
	for pair in urivars:
		key = urllib.unquote(pair[0:pair.find('=')]).decode('utf8')
		val = urllib.unquote(pair[pair.find('=') + 1:]).decode('utf8')
		if val.find(',') != -1:
			val = val.split(',')
		retdict[key] = val
	
	return retdict

class HTTPHandler(BaseHTTPRequestHandler):
	def process_request(self, basepath, urivars={}, method='get'):
		api = BaseAPIHandler()
			
		if basepath == '/schedule.json':
			basepath = '/schedule'
			urivars['format'] = 'json'
		elif basepath == '/schedule.xml':
			basepath = '/schedule'
			urivars['format'] = 'xml'
		## Chrome always tries to grab the icon.
		## Send it something so it stops raising errors in the console...
		elif basepath == '/favicon.ico':
			print "Client asking for favicon; sending it."
			self.send_response(200)
			self.send_header('Content-type', 'image/png')
			self.end_headers()
			ico = open('bus.png', 'rb')
			self.wfile.write(ico.read())
			ico.close()
			return
		
		print "= processing request =\nbasepath: %s\nurivars: %s" % (str(basepath), str(urivars))
		
		try:
			response = api.do_command(basepath, urivars)
			print '== Content-type: %s ==' % str(response[0])
			#print "== Content ==\n" + str(response[1]) + "\n== End Content =="
			self.send_response(200)
			self.send_header('Content-type', response[0])
			self.end_headers()
			self.wfile.write(response[1])
		except APIError as err:
			print str(err)
			self.send_error(err.code, err.msg)
			
		except Exception as e:
			print "Exception caught: " + str(e)
			self.send_error(500, "Server Exception: " + str(e))

	def do_GET(self):
		if self.path.find('?') != -1:
			self.process_request(self.path[:self.path.find('?')], parse_urivars(self.path[self.path.find('?') + 1:]))
		else:
			self.process_request(self.path)

	def do_POST(self):
		self.process_request(self.path, parse_urivars(self.rfile.read( int(self.headers.getheader('content-length')))), 'post')

class HTTPThread():
	def __init__(self):
		self.__bind_ip = '127.0.0.1'
		self.__bind_port = 8080
		self.server = HTTPServer( (self.__bind_ip, self.__bind_port), HTTPHandler)
		self.process = Process(target=self.server.serve_forever, args=[])
	
	def start(self):
		self.process.start()
		print 'HTTPThread process started with PID %s' % str(self.process.pid)
	
	def join(self):
		self.process.join()
	
	def run(self):
		try:
			print 'Listening on %s:%s' % (self.__bind_ip, str(self.__bind_port))
			self.server.serve_forever()

		except KeyboardInterrupt:
			print 'KeyboardInterrupt received.  Shutting down.'
			self.server.socket.close()