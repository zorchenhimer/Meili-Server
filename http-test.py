#!/usr/bin/python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

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
			self.send_header('Content-type', 'text/plain')
			self.end_headers()

			#self.wfile.write('Derp')
			f = open('../doc' + self.path)
			self.wfile.write(f.read())
			f.close()
		elif self.path.find('/status') == 0:
			self.send_response(200)
			self.send_header('Content-type', 'text/plain')
			self.end_headers()

			self.wfile.write("Server Status\n\n")
			urivars = self.path[8:].split('&')
			for pair in urivars:
				self.wfile.write(pair + "\n")

			self.wfile.write("\nUsing parse_urivars():\n")
			parsed = parse_urivars(self.path[8:])
			for key, val in parsed.iteritems():
				self.wfile.write("\t" + key + ': ' + str(val) + "\n")

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
