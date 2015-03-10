#!/usr/bin/python2

from flask import Flask, render_template, Response, abort, request, jsonify, make_response, redirect
from Lib.Data import BusArrival, BusDeparture, BusList, KeyValueData
from Lib.Database import DBCaches
from Lib.SQLite import SQLiteDB
import json
import time

server = Flask(__name__)

# TODO: Make this a fatory
db = SQLiteDB()

def json_error(message):
    return make_response(
        jsonify({'error': str(message)}),
        400
    )

class Status():
    def __init__(self):
        self.Time = None
        self.Displays = None
        self.LastUpdate = None

@server.route('/')
def debug_index():
    return render_template('debug-gui.html',
        companies=db.get_company_list(),
        cities=db.get_city_list(),
        statuses=db.get_status_list(),
        gates=db.get_gate_list(),
        arrivals=db.get_arrivals(),
        departures=db.get_departures(),
    )

@server.route('/schedule')
@server.route('/schedule.<format>')
def schedule(format='json'):
    data = None
    mime = None

    arrivals = db.get_arrivals()
    departures = db.get_departures()

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

@server.route('/add_arrival', methods=['POST'])
def add_arrival():
    args = {}
    args['company'] = request.form.get('company')
    args['city'] = request.form.get('city')
    args['time'] = request.form.get('time')
    args['status'] = request.form.get('status')

    now = request.form.get('time_now')
    ret = ''
    if now is not None:
        args['time'] = time.time()

    for key,val in args.items():
        if val is None:
            abort(json_error("Missing something"))

    dbret = db.add_arrival(args['company'], args['city'], args['time'], args['status'])
    return redirect('/', code=302)

@server.route('/add_departure', methods=['GET', 'POST'])
def add_departure():
    args = {}
    args['company'] = request.form.get('company')
    args['city'] = request.form.get('city')
    args['time'] = request.form.get('time')
    args['status'] = request.form.get('status')
    args['gate'] = request.form.get('gate')
    args['busnum'] = request.form.get('busnum')

    now = request.form.get('time_now')
    ret = ''
    if now is not None:
        args['time'] = time.time()

    for key,val in args.items():
        if key == 'busnum':
            ## This field can be blank. (should that be allowed?)
            continue
        if val is None:
            abort(json_error("Missing something"))

    dbret = db.add_departure(args['company'], args['city'], args['time'], args['status'], args['gate'], args['busnum'])
    return redirect('/', code=302)

@server.route('/add_company', methods=['GET', 'POST'])
def add_company():
    company = request.args.get('name')
    row = db.add_company(company)
    return jsonify({'id': int(row[0][0]), 'company': company})

@server.route('/modify/<bus_type>/<int:id>/', methods=['GET', 'POST'])
def modify_bus(bus_type, id):
    args = {}
    args['id'] = id
    if bus_type == 'arrival' or bus_type == 'departure':
        args['type'] = bus_type
    else:
        abort(404)

    if request.method == 'POST':
        args['id'] = request.form.get('id')
        args['type'] = request.form.get('type')
        args['city'] = request.form.get('city')
        args['company'] = request.form.get('company')
        args['time'] = request.form.get('time')
        args['status'] = request.form.get('status')

        if args['type'] == 'departure':
            args['gate'] = request.form.get('gate')
            args['busnum'] = request.form.get('busnum')
            db.modify_departure(
                    ID = args['id'],
                    city = args['city'],
                    company = args['company'],
                    time = args['time'],
                    status = args['status'],
                    gate = args['gate'],
                    number = args['busnum'],
                )
        else:
            db.modify_arrival(
                    ID = args['id'],
                    city = args['city'],
                    company = args['company'],
                    time = args['time'],
                    status = args['status'],
                )

    bus = None
    gates = []

    ## FIXME: validate this stuff.
    if args['type'] == 'arrival':
        try:
            bus = db.get_arrival_by_id(args['id'])
        except IndexError:
            abort(404)
    elif args['type'] == 'departure':
        try:
            bus = db.get_departure_by_id(args['id'])
            gates = db.get_gate_list()
        except IndexError:
            abort(404)
    else:
        abort(404)

    if bus is None:
        print("bus is None!")
        abort(404)

    return render_template('debug-modify-bus.html',
            companies = db.get_company_list(),
            cities = db.get_city_list(),
            statuses = db.get_status_list(),
            bus = bus,
            gates = gates,
            id = args['id'],
        )

@server.route('/cache')
def debug_cache():
    db.update_cache()
    cache = DBCaches()
    return str([cache.Gates, cache.Cities, cache.Statuses, cache.Companies])

@server.route('/setting')
def get_setting():
    var = request.args.get('var')
    val = db.get_setting(var)
    return jsonify({var: val})

if __name__ == '__main__':
    server.debug = True
    server.run()
