#!/usr/bin/python

import json
import xml.etree.ElementTree as ET
import time

__all__ = "BaseAIPHandler APIError".split(' ')

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
			raise APIError(400, 'Invalid command: %s' % command)
	
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
		notype = False
		
		if 'type' in vars:
			t = vars['type']
			if 'servertime' in t:
				content_struct['servertime'] = int(time.time())
			if 'lastupdate' in t:
				content_struct['lastupdate'] = int(time.time() - 1343)
			if 'displays' in t:
				content_struct['displays'] = int(4)
		else:
			notype = True
			content_struct = {"status":"General Stats - TODO"}
		
		if 'format' in vars:
			## XML formatting needs work.  Might be part of the data classes...
			if vars['format'] == 'xml':
				content_type = 'error 501'
				##encoded_content = dict_to_XML('status', content_struct)
				if 'displays' in content_struct:
					encoded_content += '<displays>%s</displays>' % str(content_struct['displays'])
				if 'lastupdate' in content_struct:
					encoded_content += '<lastupdate>%s</lastupdate>' % str(content_struct['lastupdate'])
				if 'servertime' in content_struct:
					encoded_content += '<servertime>%s</servertime>' % str(content_struct['servertime'])
				
				if notype is True:
					encoded_content = '<general>%s</general>' % str(content_struct['status'])
				
				encoded_content = "<?xml version=\"1.0\" encoding=\"utf-8\" ?>\n<status>%s</status>" % encoded_content
					
				##raise Exception("501 Not Implemented")
			elif vars['format'] == 'json':
				content_type = 'application/json'
				e = json.JSONEncoder()
				encoded_content = e.encode(content_struct)
		else:
			content_type = 'application/json'
			e = json.JSONEncoder()
			encoded_content = e.encode(content_struct)
		
		return [content_type, encoded_content]

class APIError(Exception):
	def __init__(self, code=500, msg="General error."):
		## Code is basically an HTTP code.
		self.code = int(code)
		self.msg = str(msg)
	
	def __str__(self):
		return 'APIError: [%s] %s' % (str(self.code), self.msg)