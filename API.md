# API Specification

## HTTP Passive API

- `/schedule` - Accepts the following variables. All are optional.
	- `format` - Either `json` (default) or `xml`.
	- `start` - Get buses after this time. Time formatted as a Unix timestamp.
	- `end` - Get buses before this time. Time formatted as a Unix timestamp.
	- `count` - Return this many buses at most.  Defaults to 50.
	- `status` - Only return buses with the given status, defaults to 'all'.  Miltiple statuses need to be comma delimited.  Accepted values:
		- `all` - All buses within time range.
		- `on-time` - Confirmed on time.
		- `canceled` - Confirmed canceled.
		- `boarding` - Currently boarding.
		- `delayed` - Confirmed delayed or already late.
		- `projected` - Unconfirmed on time.
		- `departed` - Bus is gone.
- `/schedule.json` - Alias for `/schedule?format=json`
- `/schedule.xml` - Alias for `/schedule?format=xml`
- `/status` - Returns general status of the server
- `/status?type={type}` - Where `{type}` is one of the following:
	- `servertime` - Current time on the server. Returned as Unix timestamp.
	- `lastupdate` - Timestamp of the last update.
	- `displays` - Return info the server has about display instances.
	- `version` - Return the API version the server is using

The following are only avalable as HTTP POST requests.  All fields are required unless otherwise specified.

- `/add_arrival` - add a new arrival to to the database.  All fields except `format` are required.
	- `company`
	- `city`
	- `time`
	- `status`
	- `format` - *Optional* - Format of the response message, either `json` or `xml`.
- `/add_departure` - add a new departure to to the database.  All fields except `format` are required.
	- `company`
	- `city`
	- `time`
	- `status`
	- `gate`
	- `busnum`
	- `format` - *Optional* - Format of the response message, either `json` or `xml`.
- `/modify` - `id` is required, all others optional.
	- `id` - ID of the bus to modify
	- `company`
	- `city`
	- `time`
	- `status`
	- `gate` - departures only
	- `busnum` - departures only
	- `format` - *Optional* - Format of the response message, either `json` or `xml`.