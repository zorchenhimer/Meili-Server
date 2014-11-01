#!/usr/bin/python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import time
import urllib
import json
import xml.etree.ElementTree as ET

PORT_NUMBER = 8080

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

## FFFFFFFFFUUUUUUUUUUu
def dict_to_XML(rootname, struct):
	print "Attempting to encode " + str(struct) + " into XML with root " + str(rootname)
	root = ET.Element(rootname)
	for key in struct:
		var = struct[key]
		if type(var) is type(dict()):
			e = ET.SubElement(root, key)
			_rabbit_hole_dict(e, key, var)
		elif type(var) is type(list()):
			for item in var:
				e = ET.SubElement(root, key)
				e.text = item
	print "Finished attempt: " + str(ET.dump(root))
	return ET.dump(root)

def _rabbit_hole_dict(parent, name, struct):
	for key, var in struct:
		if type(var) is type(dict()):
			e = ET.SubElement(parent, _rabbit_hole_dict(key, var))
		elif type(var) is type(list()):
			for item in var:
				e = ET.SubElement(parent, key)
				e.text = item
				## TODO: rabbithole for lists

class BaseAPIHandler():
	def __init__(self):
		self.__commands = {
			'schedule': self.cmd_schedule,
			'status':	self.cmd_status
		}
	
	## Returns array: [content-type, content]
	def do_command(self, command, vars):
		## Check for `command` in self._commands
		##   if exists, call function
		if command.find('/') == 0:
			command = command[1:]
		if command in self.__commands:
			return self.__commands[command](vars)
		else:
			raise Exception('Invalid command: %s' % command)
	
	def cmd_schedule(self, vars):
		## Return the schedule according to `vars`
		print 'schedule vars: %s' % str(vars)
		path = ''
		content_type = ''
		content = ''
		if 'format' in vars:
			if vars['format'] == 'xml':
				path = '../doc/schedule.xml'
				content_type = 'text/xml'
			elif vars['format'] == 'json':
				content_type = 'application/json'
				path = '../doc/schedule.json'
		else:
			content_type = 'application/json'
			path = '../doc/schedule.json'

		f = open(path, 'r')
		content = f.read()
		f.close()
		
		return [content_type, content]
	
	def cmd_status(self, vars):
		## Return the status according to `vars`
		content_type = ''
		content_struct = {}
		encoded_content = ''
		
		if 'type' in vars:
			t = vars['type'].split(',')
			if 'servertime' in t:
				content_struct['servertime'] = int(time.time())
			if 'lastupdate' in t:
				content_struct['lastupdate'] = int(time.time() - 1343)
			if 'displays' in t:
				content_struct['displays'] = int(4)
		else:
			content_struct = {"status":"General Stats - TODO"}
		
		if 'format' in vars:
			if vars['format'] == 'xml':
				##content_type = 'error 501'
				##encoded_content = dict_to_XML('status', content_struct)
				raise Exception("501 Not Implemented")
			elif vars['format'] == 'json':
				content_type = 'application/json'
				e = json.JSONEncoder()
				encoded_content = e.encode(content_struct)
		else:
			content_type = 'application/json'
			e = json.JSONEncoder()
			encoded_content = e.encode(content_struct)
		
		return [content_type, encoded_content]

class TestHandler(BaseHTTPRequestHandler):
	def process_request(self, basepath, urivars={}, method='get'):
		api = BaseAPIHandler()
			
		if basepath == '/schedule.json':
			basepath = '/schedule'
			urivars['format'] = 'json'
		elif basepath == '/schedule.xml':
			basepath = '/schedule'
			urivars['format'] = 'xml'
		
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
			# hacky, i know. should really be a costom exception.
			num = 400
			msg = str(e)
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
	server = HTTPServer( ('', PORT_NUMBER), TestHandler)
	print 'Listening on ', PORT_NUMBER

	server.serve_forever()

except KeyboardInterrupt:
	print 'KeyboardInterrupt received.  Shutting down.'

finally:
	server.socket.close()
