#!/usr/bin/python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urllib
from Lib.API import BaseAPIHandler

PORT_NUMBER = 8081
BIND_IP = '127.0.0.1'

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

class TestHandler(BaseHTTPRequestHandler):
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
			print "== Content ==\n" + str(response[1]) + "\n== End Content =="
			self.send_response(200)
			self.send_header('Content-type', response[0])
			self.end_headers()
			self.wfile.write(response[1])
		except Exception as e:
			# hacky, i know. should really be a custom exception.
			num = 400
			msg = str(e)
			print "Exception caught: " + msg
			if str(e).find(' '):
				num = int(str(e)[:str(e).find(' ')])
				msg = str(e)[str(e).find(' ') + 1:]
				
			self.send_error(num, msg)

	def do_GET(self):
		if self.path.find('?') != -1:
			self.process_request(self.path[:self.path.find('?')], parse_urivars(self.path[self.path.find('?') + 1:]))
		else:
			self.process_request(self.path)

	def do_POST(self):
		self.process_request(self.path, parse_urivars(self.rfile.read( int(self.headers.getheader('content-length')))), 'post')

try:
	server = HTTPServer( (BIND_IP, PORT_NUMBER), TestHandler)
	print 'Listening on %s:%s' % (BIND_IP, str(PORT_NUMBER))

	server.serve_forever()

except KeyboardInterrupt:
	print 'KeyboardInterrupt received.  Shutting down.'

finally:
	server.socket.close()
