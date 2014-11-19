#!/usr/bin/python2

import sqlite3 as lite
import time

class BaseDB():
	def __init__(self):
		pass
	
	def set_connection(self):
		## For sqlite, this would be just a filename.  For something like MySQL, this would be server/user/pass stuff.
		raise NotImplementedError
	
	def get_setting(self, name):
		raise NotImplementedError
		
	## Default time range from 'now' until 'now + 5 hours'
	def get_arrivals(self, start_range=time.time(), end_range=(time.time() + (60 * (60 * 5))), max_returned=50, filter_status=None, cleared=False):
		raise NotImplementedError
	
	def get_departures(self, start_range=time.time(), end_range=(time.time() + (60 * (60 * 5))), max_returned=50, filter_status=None, cleared=False):
		raise NotImplementedError
	
	def add_gate(self, gate_name):
		raise NotImplementedError
	
	def add_status(self, status_name):
		raise NotImplementedError
	
	def add_city(self, city_name):
		raise NotImplementedError
	
	def add_company(self, company_name):
		raise NotImplementedError
	
	def add_arrival(self, company, city, time, status):
		raise NotImplementedError
	
	def add_departure(self, company, city, time, status, gate, number):
		raise NotImplementedError
	
	def modify_arrival(self, id, company=None, city=None, time=None, status=None):
		raise NotImplementedError
	
	def modify_departure(self, id, company=None, city=None, time=None, status=None, gate=None, number=None):
		raise NotImplementedError
	
	def modify_gate(self, id, gate_name):
		raise NotImplementedError
	
	def modify_status(self, id, status_name):
		raise NotImplementedError
	
	def modify_city(self, id, city_name):
		raise NotImplementedError
	
	def modify_company(self, id, company_name):
		raise NotImplementedError

class SQLiteDB(BaseDB):
	def __init__(self):
		self.dbfile = 'archive.db'
		self.conn = None
		self.LastRowcount = 0
	
	def init_db(self):
		sql_file = open('dbinit.sql', 'r')
		sql_text = sql_file.read()
		sql_file.close()

		self.__open_connection()
		with self.conn:
			cur = self.conn.cursor()
			cur.executescript(sql_text)

	def set_connecton(self, db_file):
		self.dbfile = db_file
	
	def get_setting(self, name):
		query = 'SELECT value FROM settings WHERE name=?'
		ret = self.__run_query(query, name)
		if len(ret) == 0:
			return None
		else:
			return ret[0][0]

	def set_setting(self, name, value):
		query = 'INSERT OR REPLACE INTO settings (name, value) VALUES (?, ?)'
		self.__run_query(query, name, value)

	def __run_query(self, query, *args):
		rows = None
		self.__open_connection()
		with self.conn:
			cur = self.conn.cursor()
			cur.execute(query, args)
			self.LastRowcount = cur.rowcount
			rows = cur.fetchall()
		return rows
	
	def __open_connection(self):
		self.conn = lite.connect(self.dbfile)

