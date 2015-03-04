#!/usr/bin/python2

import sqlite3 as lite
import os
import time
import Lib.Data as Data
from Lib.Misc import singleton

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

    def get_arrival_by_id(self, id):
        raise NotImplementedError

    def get_departure_by_id(self, id):
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

    def modify_arrival(self, ID, company=None, city=None, time=None, status=None):
        raise NotImplementedError

    def modify_departure(self, ID, company=None, city=None, time=None, status=None, gate=None, number=None):
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

    def get_company_id(self, company):
        cache = DBCaches()
        ## Update if cache is older than an hour.
        if cache.LastUpdate > time.time() - (60*60) or cache.Companies == None:
            self.update_cache()

        co = None
        if company.isdigit():
            for c in cache.Companies:
                if c.id == int(company):
                    co = c.id
                    break
        else:
            for c in cache.Companies:
                if c.value.lower() == company.lower():
                    co = c.id
                    break
        if co is None:
            raise Exception("Company with id or value '{iv}' not found!".format(iv=company))
        return co

    def get_city_id(self, city):
        cache = DBCaches()
        ## Update if cache is older than an hour.
        if cache.LastUpdate > time.time() - (60*60) or cache.Cities == None:
            self.update_cache()

        ci = None
        if city.isdigit():
            for c in cache.Cities:
                if c.id == int(city):
                    ci = c.id
                    break
        else:
            for c in cache.Cities:
                if c.value.lower() == city.lower():
                    ci = c.id
                    break
        if ci is None:
            raise Exception("City with id or value '{iv}' not found!".format(iv=city))
        return ci

    def get_status_id(self, status):
        cache = DBCaches()
        ## Update if cache is older than an hour.
        if cache.LastUpdate > time.time() - (60*60) or cache.Statuses == None:
            self.update_cache()

        st = None
        if status.isdigit():
            for s in cache.Statuses:
                if s.id == int(status):
                    st = s.id
                    break
        else:
            for s in cache.Statuses:
                if s.lower() == status.lower():
                    st = s.id
                    break
        if st is None:
            raise Exception("Status with id or value '{iv}' not found!".format(iv=status))
        return st

    def get_gate_id(self, gate):
        cache = DBCaches()
        ## Update if cache is older than an hour.
        if cache.LastUpdate > time.time() - (60*60) or cache.Gates == None:
            self.update_cache()

        gt = None
        if gate.isdigit():
            for s in cache.Gates:
                if s.id == int(gate):
                    gt = s.id
                    break
        else:
            for s in cache.Gates:
                if s.lower() == gate.lower():
                    gt = s.id
                    break
        if gt is None:
            raise Exception("Gate with id or value '{iv}' not found!".format(iv=gate))
        return gt

    ## Janitorial stuff.  Times are in minutes.
    def update_delayed(self, time_threshold = 1):
        raise NotImplementedError

    def clear_canceled(self, time_threshold = 20):
        raise NotImplementedError

    ## Arrived and departed
    def clear_done(self, time_threshold = 20):
        raise NotImplementedError

    def update_caches(self):
        raise NotImplementedError

@singleton
class DBCaches():
    def __init__(self):
        self.Gates = None
        self.Cities = None
        self.Statuses = None
        self.Companies = None
        self.LastUpdate = None
