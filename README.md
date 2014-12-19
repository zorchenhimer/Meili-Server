# Meili - Server
This is the server component to the Meili Arrival and Departure system.  The
server is not fully functional yet, but progress is being made.

# Server Responsibilities
The server stores all arrival and departure records as well as company names,
city names, and gate names.  At this point, any and all changes to any of
these records is done through the HTTP API.  Only debugging and testing HTML
pages will be served from the server.

# Design
All design documents are in the `doc` folder in root of this repository.  This includes the HTTP API
specifiction as well as example JSON and XML files in the format produced by
the server.