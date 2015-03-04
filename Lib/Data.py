#!/usr/bin/python

import datetime

class BusStatus():
    UNKNOWN = 0
    ONTIME = 1
    DELAYED = 2
    PROJECTED = 4
    BOARDING = 5

class KeyValueData(object):
    def __init__(self, id, value):
        self.id = id
        self.value = value

    def __str__(self):
        return '{i}: {v}'.format(i=self.id, v=self.value)

    def __unicode__(self):
        return self.__str__()

    def __repr__(self):
        return self.__str__()

class BusList(list):
        def append_bus(self, data):
            self.append(data)
            self.sort(None, key=data.Time)

        def clear(self):
            del self[:]

        def get_dict(self):
            ret_list = []
            for b in self:
                ret_list.append(b.get_dict())
            return ret_list

class BusBase():
    def __init__(self, company, city, time, status, ID):
        self.ID = ID
        self.Company = company
        self.City = city        ## Destination/Origin
        self.Time = time        ## Departure/Arrival time
        self.Status = status
        self.is_arrival = False
        self.is_departure = False

    @property
    def TimeString(self):
        #return time.strftime('%H:%M:%S', self.Time)
        return datetime.datetime.fromtimestamp(int(self.Time)).strftime('%H:%M:%S')

    def update_status(self, status):
        ## FIXME: input validation!
        self.Status = status

    def to_string(self):
        return str(self.get_dict())

    def get_dict(self):
        ret_dict = { "company": self.Company,
                     "city": self.City,
                     "time": self.Time,
                     "status": self.Status }
        if isinstance(self, BusDeparture):
            ret_dict["busnum"] = self.Number
            ret_dict["gate"] = self.Gate

        return ret_dict
    def __str__(self):
        return self.to_string()

class BusArrival(BusBase):
    def __init__(self, company, city, time, status, ID):
        BusBase.__init__(self, company, city, time, status, ID)
        self.is_arrival = True

class BusDeparture(BusBase):
    def __init__(self, company, city, time, status, gate, number, ID):
        BusBase.__init__(self, company, city, time, status, ID)
        self.Number = number
        self.Gate = gate
        self.is_departure = True
