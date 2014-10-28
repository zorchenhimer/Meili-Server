#!/usr/bin/python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import time

PORT_NUMBER = 8080

def parse_urivars(varstring):
	## varstring is the uri minus everything before, and including, the '?'.
	retdict = {}
	urivars = varstring.split('&')
	for pair in urivars:
		key = pair[0:pair.find('=')]
		val = pair[pair.find('=') + 1:]
		if val.find(',') != -1:
			val = val.split(',')
		retdict[key] = val
	
	return retdict

class TestHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		if self.path == '/schedule.json' or self.path == '/schedule.xml':
			self.send_response(200)
			if self.path[-4:] == '.xml':
				self.send_header('Content-type', 'text/xml')
			else:
				self.send_header('Content-type', 'text/plain')
			self.end_headers()

			#self.wfile.write('Derp')
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
					if urivars['type'] == 'servertime':
						retmsg = str(int(time.time()))
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

try:
	server = HTTPServer( ('', PORT_NUMBER), TestHandler)
	print 'Listening on ', PORT_NUMBER

	server.serve_forever()

except KeyboardInterrupt:
	print 'KeyboardInterrupt received.  Shutting down.'
	server.socket.close()
