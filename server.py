#!/usr/bin/python2

from flask import Flask, render_template, Response, abort, request, jsonify, make_response
from Lib.Data import BusArrival, BusDeparture, BusList
from Lib.Database import SQLiteDB, DBCaches
import json
import time

server = Flask(__name__)
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
    vars = {}
    vars['company'] = request.form.get('company')
    vars['city'] = request.form.get('city')
    vars['time'] = request.form.get('time')
    vars['status'] = request.form.get('status')

    now = request.form.get('time_now')
    ret = ''
    if now is not None:
        vars['time'] = time.time()

    for key,val in vars.items():
        if val is None:
            abort(json_error("Missing something"))

    dbret = db.add_arrival(vars['company'], vars['city'], vars['time'], vars['status'])
    return str(dbret)

@server.route('/add_departure', methods=['GET', 'POST'])
def add_departure():
    vars = {}
    vars['company'] = request.form.get('company')
    vars['city'] = request.form.get('city')
    vars['time'] = request.form.get('time')
    vars['status'] = request.form.get('status')
    vars['gate'] = request.form.get('gate')
    vars['busnum'] = request.form.get('busnum')

    now = request.form.get('time_now')
    ret = ''
    if now is not None:
        vars['time'] = time.time()

    for key,val in vars.items():
        if key == 'busnum':
            ## This field can be blank. (should that be allowed?)
            continue
        if val is None:
            abort(json_error("Missing something"))

    dbret = db.add_departure(vars['company'], vars['city'], vars['time'], vars['status'], vars['gate'], vars['busnum'])
    return str(dbret)
    #raise NotImplementedError

@server.route('/add_company', methods=['GET', 'POST'])
def add_company():
    company = request.args.get('name')
    row = db.add_company(company)
    return jsonify({'id': int(row[0][0]), 'company': company})

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
