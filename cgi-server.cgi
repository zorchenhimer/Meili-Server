#!/usr/bin/python

from wsgiref.handlers import CGIHandler
from server import server

server.debug = False
GCIHandler().run(server)
