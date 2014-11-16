#!/usr/bin/python2

from flask import Flask, render_template, Response, abort
from Lib.Data import BusArrival, BusDeparture, BusList
import json
import time

server = Flask(__name__)

arrivals = BusList()
departures = BusList()
json_dict = None

# Temporary until I connect a database.
def parse_json_source():
	jfile = open('../doc/schedule.json', 'r')
	json_dict = json.load(jfile)
	jfile.close()

	arrivals.clear()
	departures.clear()

	for arrival in json_dict['arrivals']:
		arrivals.append(
			BusArrival(
				arrival['company'],
				arrival['city'],
				arrival['time'],
				arrival['status'])
		)
	
	for departure in json_dict['departures']:
		departures.append(
			BusDeparture(
				departure['company'],
				departure['city'],
				departure['time'],
				departure['status'],
				departure['gate'],
				departure['busnum'])
		)

class Status():
	def __init__(self):
		self.Time = None
		self.Displays = None
		self.LastUpdate = None

@server.route('/schedule')
@server.route('/schedule.<format>')
def xml_schedule(format='json'):
	parse_json_source()
	data = None
	mime = None
	if format == 'xml':
		data = render_template('api/schedule.xml', arrivals=arrivals, departures=departures)
		mime = 'text/xml'
	elif format == 'json':
		data = json.dumps({'departures': departures.get_dict(), 'arrivals': arrivals.get_dict()})
		mime = 'text/plain'
	else:
		abort(404)
	return Response(data, mimetype=mime)

@server.route('/status')
def status():
	st = Status()
	st.Time = int(time.time())
	st.Displays = 5
	st.LastUpdate=int(time.time() + 100)
	xml = render_template('api/status.xml', status=st)
	return Response(xml, mimetype="text/xml")

@server.route('/favicon.ico')
def favicon():
	return server.send_static_file('bus.png')

if __name__ == '__main__':
	server.debug = True
	server.run()
