#!/usr/bin/python2

import sqlite3 as sql
import sys
import random
import time
import datetime
from Lib.Database import SQLiteDB

con = sql.connect('archive.db')

def init_db():
	with con:
		cur = con.cursor()
		cur.execute('drop table if exists settings')
		cur.execute('create table settings(id INTEGER PRIMARY KEY, name text, value text)')
		cur.execute('insert into settings (name, value) values("apiversion", "1")')
		
		cur.execute('drop table if exists arrivals')
		cur.execute('create table arrivals(id integer primary key, company int, city int, time int, status int, clear int default 0)')
		
		cur.execute('drop table if exists departures')
		cur.execute('create table departures(id integer primary key, company int, city int, time int, status int, gate int, number text, clear int default 0)')
		
		cur.execute('drop table if exists statuses')
		cur.execute('create table statuses(id integer primary key, status text)')
		
		cur.execute('drop table if exists cities')
		cur.execute('create table cities(id integer primary key, city text)')
		
		cur.execute('drop table if exists companies')
		cur.execute('create table companies(id integer primary key, company text)')
		
		cur.execute('drop table if exists gates')
		cur.execute('create table gates(id integer primary key, gate text)')

def add_dummy_data():
	r = random.Random()
	cities = 'New York,Boston,New London,China Town,Flushing,Dorchester,Danbury,Crasnton,Providence'.split(',')
	companies = 'Greyhound,CK Tours,Trans-Pacific,Anna,Win Li Tours,ECS,Treblays'.split(',')
	statuses = 'on time,canceled,boarding,delayed,projected'.split(',')
	gates = []
	gletters = 'abc'
	gnumbers = '12345'
	for l in gletters:
		for n in gnumbers:
			gates.append(str(l+n))
			
	with con:
		cur = con.cursor()
		sqlquery = 'insert into %s (%s) values ("%s")'
		
		for c in cities:
			cur.execute(sqlquery % ('cities', 'city', c))
		
		for c in companies:
			cur.execute(sqlquery % ('companies', 'company', c))
		
		for s in statuses:
			cur.execute(sqlquery % ('statuses', 'status', s))
		
		for g in gates:
			cur.execute(sqlquery % ('gates', 'gate', g))
			
		for n in range(5):
			city = r.randint(1, len(cities))
			company = r.randint(1, len(companies))
			status = r.randint(1, len(statuses))
			t = int(time.time()) + (r.randint(0, 60) * 60)
			print "[Arrival] city: %s; company: %s; status: %s; time: %s" % (str(city), str(company), str(status), str(t))
			cur.execute('insert into arrivals (city, company, status, time) values (%s, %s, %s, %s)' % (city, company, status, t))
		
		for n in range(5):
			city = r.randint(1, len(cities))
			company = r.randint(1, len(companies))
			status = r.randint(1, len(statuses))
			gate = r.randint(1, len(gates))
			number = gates[r.randint(0, len(gates) - 1)]
			t = int(time.time()) + (r.randint(0, 60) * 60)
			
			cur.execute('insert into departures (city, company, status, time, gate, number) values (%s, %s, %s, %s, %s, "%s")' % (city, company, status, t, gate, number))

#print "Initializing database..."
#init_db()

#print "Inserting dummy values..."
#add_dummy_data()
#print "done"

db = SQLiteDB()
#db.init_db()
print str(db.get_setting('apiversion'))
print str(db.get_setting('Mr Name'))
db.set_setting('Other Name', 'Bob')
print str(db.get_setting('Other Name'))

