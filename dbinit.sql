DROP TABLE IF EXISTS settings;
CREATE TABLE settings(name TEXT PRIMARY KEY, value TEXT);
INSERT INTO settings (name, value) VALUES("apiversion", "1");

DROP TABLE IF EXISTS arrivals;
CREATE TABLE arrivals(id INTEGER PRIMARY KEY, company INTEGER, city INTEGER, time INTEGER, status INTEGER, clear INTEGER DEFAULT 0);

DROP TABLE IF EXISTS departures;
CREATE TABLE departures(id INTEGER PRIMARY KEY, company INTEGER, city INTEGER, time INTEGER, status INTEGER, gate INTEGER, busnum TEXT, clear INT DEFAULT 0);

DROP TABLE IF EXISTS statuses;
CREATE TABLE statuses(id INTEGER PRIMARY KEY, status TEXT);

DROP TABLE IF EXISTS cities;
CREATE TABLE cities(id INTEGER PRIMARY KEY, city TEXT);

DROP TABLE IF EXISTS companies;
CREATE TABLE companies(id INTEGER PRIMARY KEY, company TEXT);

DROP TABLE IF EXISTS gates;
CREATE TABLE gates(id INTEGER PRIMARY KEY, gate TEXT);

INSERT INTO statuses (status) VALUES ("Projected"), ("On Time"), ("Delayed"), ("Canceled"),
                                     ("Boarding"), ("Departed");
