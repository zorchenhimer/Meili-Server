#!/usr/bin/python

import datetime

class BusStatus():
    UNKNOWN = 0
    ONTIME = 1
    DELAYED = 2
    CANCELED = 3
    PROJECTED = 4
    BOARDING = 5

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

    @property
    def TimeString(self):
        #return time.strftime('%H:%M:%S', self.Time)
        return datetime.datetime.fromtimestamp(int(self.Time)).strftime('%H:%M:%S')

    def update_status(self, status):
        ## FIXME: input validation!
        self.Status = status

    def to_string(self):
        return str([self.ID, self.Company, self.Status, self.Time, self.City])

    def is_arrival(self):
        raise NotImplementedError

    def is_departure(self):
        raise NotImplementedError

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

    def is_arrival(self):
        return True

    def is_departure(self):
        return False

class BusDeparture(BusBase):
    def __init__(self, company, city, time, status, gate, number, ID):
        BusBase.__init__(self, company, city, time, status, ID)
        self.Number = number
        self.Gate = gate

    def to_string(self):
        return BusBase.to_string(self) + ' ' + str([self.Number, self.Gate])

    def is_arrival(self):
        return False

    def is_departure(self):
        return True
