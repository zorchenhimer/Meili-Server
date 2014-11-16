#!/usr/bin/python2

from flask import Flask, render_template, Response
from Lib.Data import BusArrival, BusDeparture, BusList
import json
import time

server = Flask(__name__)

arrivals = BusList()
departures = BusList()

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

@server.route('/schedule.xml')
def xml_schedule():
	parse_json_source()
	xml = render_template('schedule.xml', arrivals=arrivals, departures=departures)
	return Response(xml, mimetype="text/xml")

@server.route('/status')
def status():
	st = Status()
	st.Time = int(time.time())
	xml = render_template('status.xml', status=st)
	return Response(xml, mimetype="text/xml")

if __name__ == '__main__':
	server.debug = True
	server.run()
