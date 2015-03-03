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

    ## Janitorial stuff.  Times are in minutes.
    def update_delayed(self, time_threshold = 1):
        raise NotImplementedError

    def clear_canceled(self, time_threshold = 20):
        raise NotImplementedError

    ## Arrived and departed
    def clear_done(self, time_threshold = 20):
        raise NotImplementedError

@singleton
class DBCaches():
    def __init__(self):
        self.Gates = None
        self.Cities = None
        self.Statuses = None
        self.Companies = None
        self.LastUpdate = None
