#!/usr/bin/python2

import sqlite3 as lite
import os
import time
import Data

def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

class BaseDB(object):
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

    def get_city_list(self):
        raise NotImplementedError

    def get_company_list(self):
        raise NotImplementedError

    def get_status_list(self):
        raise NotImplementedError

    def get_gate_list(self):
        raise NotImplementedError

@singleton
class SQLiteDB(BaseDB):
    def __init__(self):
        self.dbfile = 'archive.db'
        self.conn = None
        self.LastRowcount = 0

        if os.path.isfile(self.dbfile) is False:
            print("Initializing database...");
            self.init_db()

    def init_db(self):
        sql_file = open('dbinit.sql', 'r')
        sql_text = sql_file.read()
        sql_file.close()

        #self.__open_connection()
        self.conn = lite.connect(self.dbfile)
        with self.conn:
            cur = self.conn.cursor()
            cur.executescript(sql_text)

    def set_connecton(self, db_file):
        self.dbfile = db_file

    def get_arrivals(self, start_range=time.time(), end_range=(time.time() + (60 * (60 * 5))), max_returned=50, filter_status=[], cleared=False):
        if type(False) != type(cleared):
            raise TypeError('"cleared" argument is invalid type.  Received: ' + str(type(cleared)))

        ## TODO: hard code a max? in a config file maybe?
        if type(max_returned) != int:
            raise TypeError('"max_returned" argument is invalid type. Received: ' + str(type(max_returned)))
        elif max_returned < 1:
            raise IndexError('"max_returned is less than 1!')

        query = """
SELECT
    arrivals.id, arrivals.time,
    cities.city, companies.company,
    statuses.status, arrivals.clear
FROM
    arrivals
LEFT JOIN companies
    ON arrivals.company = companies.id
LEFT JOIN cities
    ON arrivals.city = cities.id
LEFT JOIN statuses
    ON arrivals.status = statuses.id"""
        ret = self.__run_query(query)
        arrivals = Data.BusList()
        for row in ret:
            arrivals.append(
                Data.BusArrival(
                    row[3],    # Company
                    row[2], # City
                    row[1], # Time
                    row[4] # Status
                )
            )
        return arrivals

    ## TODO: filters
    def get_departures(self):
        query = """
SELECT
    departures.id, departures.time,
    departures.busnum, cities.city,
    companies.company, statuses.status,
    gates.gate, departures.clear
FROM
    departures
LEFT JOIN companies
    ON departures.company = companies.id
LEFT JOIN cities
    ON departures.city = cities.id
LEFT JOIN statuses
    ON departures.status = statuses.id
LEFT JOIN gates
    ON departures.gate = gates.id"""
        ret = self.__run_query(query)
        departures = Data.BusList()
        for row in ret:
            departures.append(
                Data.BusDeparture(
                    row[4], # Company
                    row[3], # City
                    row[1], # Time
                    row[5], # Status
                    row[6], # Gate
                    row[2] # Number
                )
            )
        return departures

    def add_arrival(self, company, city, time, status):
        if company.isdigit():
            co = int(company)
        else:
            co = self.get_company_id(company)

        if city.isdigit():
            ci = int(city)
        else:
            ci = self.get_city_id(city)

        if status.isdigit():
            st = int(status)
        else:
            st = self.get_status_id(status)

        query = 'INSERT INTO arrivals (company, city, time, status) VALUES (?, ?, ? ,?)'
        return self.__run_query(query, co, ci, int(time), st)

    def add_departure(self, company, city, time, status, gate, busnum):
        if company.isdigit():
            co = int(company)
        else:
            co = self.get_company_id(company)

        if city.isdigit():
            ci = int(city)
        else:
            ci = self.get_city_id(city)

        if status.isdigit():
            st = int(status)
        else:
            st = self.get_status_id(status)

        if gate.isdigit():
            gt = int(gate)
        else:
            gt = self.get_gate_id(gate)

        query = 'INSERT INTO departures (company, city, time, status, gate, busnum) VALUES (?, ?, ? ,?, ?, ?)'
        return self.__run_query(query, co, ci, int(time), st, gt, busnum)

    def get_company_id(self, company):
        cache = DBCaches()
        ## Update if cache is older than an hour.
        if cache.LastUpdate > time.time() - (60*60) or cache.Companies == None:
            self.update_cache()

        co = None
        for row in cache.Companies:
            if row[1].lower() == company.lower():
                co = row[0]
                break
            co = self.add_company(company)
            cache.LastUpdate = 0    # Force update on next check
        return co

    def get_city_id(self, city):
        cache = DBCaches()
        ## Update if cache is older than an hour.
        if cache.LastUpdate > time.time() - (60*60) or cache.Cities == None:
            self.update_cache()

        ci = None
        for row in cache.Cities:
            if row[1].lower() == city.lower():
                ci = row[0]
                break
            ci = self.add_city(city)
            cache.LastUpdate = 0    # Force update on next check
        return ci

    def get_status_id(self, status):
        cache = DBCaches()
        ## Update if cache is older than an hour.
        if cache.LastUpdate > time.time() - (60*60) or cache.Statuses == None:
            self.update_cache()

        st = None
        for row in cache.Statuses:
            if row[1].lower() == status.lower():
                st = row[0]
                break
            #self.add_status(status)
            #cache.LastUpdate = 0    # Force update on next check
            raise Excetpion("Invalid status in get_status_id(): '%s'" % str(status))
        return st

    def add_company(self, company):
        query_add = 'INSERT INTO companies (company) VALUES (?)'
        query_get = 'SELECT id FROM companies WHERE company = ?'
        self.__run_query(query_add, company)
        id = self.__run_query(query_get, company)
        self.conn.commit()
        return id[0][0]

    def add_city(self, city):
        query_add = 'INSERT INTO cities (city) VALUES (?)'
        query_get = 'SELECT id FROM cities WHERE city = ?'
        self.__run_query(query_add, city)
        id = self.__run_query(query_get, city)
        self.conn.commit()
        return id[0][0]

    def add_gate(self, gate):
        query_add = 'INSERT INTO gates (gate) VALUES (?)'
        query_get = 'SELECT id FROM gates WHERE gate = ?'
        self.__run_query(query_add, gate)
        id = self.__run_query(query_get, gate)
        self.conn.commit()
        return id[0][0]

    ## Not so sure if this is a good idea or not...
    def add_status(self, status):
        raise NotImplementedError
        query = 'INSERT INTO statuses (status) VALUES (?); SELECT id FROM statuses WHERE status = "?"'
        return self.__run_query(query, status, status)

    def get_city_list(self):
        query = 'SELECT id, city FROM cities'
        return self.__run_query(query)

    def get_company_list(self):
        query = 'SELECT id, company FROM companies'
        return self.__run_query(query)

    def get_status_list(self):
        query = 'SELECT id, status FROM statuses'
        return self.__run_query(query)

    def get_gate_list(self):
        query = 'SELECT id, gate FROM gates'
        return self.__run_query(query)

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

    def update_cache(self):
        cache = DBCaches()
        cache.Gates = self.__run_query('SELECT * FROM gates')
        cache.Companies = self.__run_query('SELECT * FROM companies')
        cache.Statuses = self.__run_query('SELECT * FROM statuses')
        cache.Cities = self.__run_query('SELECT * FROM cities')
        cache.LastUpdate = time.time()

    def __run_query(self, query, *args):
        rows = None
        self.conn = lite.connect(self.dbfile)
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(query, args)
            self.LastRowcount = cur.rowcount
            rows = cur.fetchall()
        return rows

@singleton
class DBCaches():
    def __init__(self):
        self.Gates = None
        self.Cities = None
        self.Statuses = None
        self.Companies = None
        self.LastUpdate = None
