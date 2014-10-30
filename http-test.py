#!/usr/bin/python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import time
import urllib

PORT_NUMBER = 8080

def parse_urivars(varstring):
	## varstring is the uri minus everything before, and including, the '?'.
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
		print 'urivars: %s' % str(urivars) + "\n"
		if basepath == '/schedule.json' or basepath == '/schedule.xml':
			self.send_response(200)
			if basepath[-4:] == '.xml':
				self.send_header('Content-type', 'text/xml')
			else:
				self.send_header('Content-type', 'text/plain')
			self.end_headers()

			f = open('../doc' + basepath)
			self.wfile.write(f.read())
			f.close()
		elif basepath == '/status':
			error = True
			retmsg = ''

			if len(urivars) == 0:
				error = False
				retmsg = 'General stats\n\nTODO\n'
			elif 'type' in urivars:
				if 'servertime' in urivars['type']:
					retmsg += str(int(time.time())) + "\n"
					error = False
				if 'lastupdate' in urivars['type']:
					retmsg += str(int(time.time()) - 245) + "\n"
					error = False
				if 'displays' in urivars['type']:
					retmsg += str(4) + "\n"
					error = False

			if error == True:
				self.send_error(400, 'Invalid query: %s' % str(urivars))
			else:
				self.send_response(200)
				self.send_header('Content-type', 'text/plain')
				self.end_headers()
				self.wfile.write(retmsg)
		
		else:
			self.send_error(404, 'File Not Found: %s' % basepath)


	def do_GET(self):
		if self.path.find('?') != -1:
			self.process_request(self.path[:self.path.find('?')], parse_urivars(self.path[self.path.find('?') + 1:]))
		else:
			self.process_request(self.path)

		"""
		if self.path == '/schedule.json' or self.path == '/schedule.xml':
			self.send_response(200)
			if self.path[-4:] == '.xml':
				self.send_header('Content-type', 'text/xml')
			else:
				self.send_header('Content-type', 'text/plain')
			self.end_headers()

			f = open('../doc' + self.path)
			self.wfile.write(f.read())
			f.close()

		elif self.path.find('/status') == 0:
			error = False
			retmsg = ""

			if self.path.find('?') == 7:
				urivars = parse_urivars(self.path[8:])
				if 'type' not in urivars:
					error = True
				else:
					types = urivars.split(',')
					if 'servertime' in types:
						retmsg = str(int(time.time()))
					elif 'lastupdate' in types:
						retmsg = str(int(time.time()-134))
					elif 'displays' in types:
						retmsg = str(4)
					else:
						error = True
			else:
				retmsg = "General Stats\n\nTODO"
			
			if error == False:
				self.send_response(200)
				self.send_header('Content-type', 'text/plain')
				self.end_headers()
				self.wfile.write(retmsg)
			else:
				self.send_error(400, 'Invalid query: %s' % str(urivars))

		else:
			self.send_error(404, 'File Not Found: %s' % self.path)
		return
		"""
	
	def do_POST(self):
		self.process_request(self.path, parse_urivars(self.rfile.read( int(self.headers.getheader('content-length')))), 'post')
		"""
		if self.path == '/posted':
			self.send_response(200)
			self.send_header('Content-type', 'text/plain')
			self.end_headers()
			
			poststr = self.rfile.read( int( self.headers.getheader('content-length') ) )
			vars = parse_urivars(poststr)
			
			self.wfile.write(self.headers)
			self.wfile.write("\n\n" + str(vars))
		else:
			self.send_error(404, 'File Not Found: %s' % self.path)
		"""

try:
	server = HTTPServer( ('', PORT_NUMBER), TestHandler)
	print 'Listening on ', PORT_NUMBER

	server.serve_forever()

except KeyboardInterrupt:
	print 'KeyboardInterrupt received.  Shutting down.'

finally:
	server.socket.close()
