#!/usr/bin/env python

import flask
from flask import Response, request, send_file
import json
import sqlite3
import csv

# Create the application.
app = flask.Flask(__name__)

@app.route('/')
def index():
	"""
	Displays the home page that leads users into different pages
	"""
	return flask.render_template('index.html')

@app.route('/appoints')
def appoints():
	format_ = request.args.get("format", None)
	appointee = request.args.get("name", "")
	appointyear = request.args.get("appointyear", "")
	appointparty = request.args.get("appointparty", "")
	appointgender = request.args.get("appointgender", "")

	# 1. Assign variable to database
	# 2. (Maybe?) Use dictionary function
	# 3. (Maybe?) Cursor variable
	# 4. Create string for SQL command with unknowns
	# 5. Initialize empty strings for SQL command

	if appointee:
		pass
		# Change empty string command (#5)

	# Use % to complete SQL command (with limit statement)

	if appointee:
		pass
		# Execute the command using cursor.execute
	else:
		pass
		# Execute without the specified query (drop-downs only)
	# Assign variable for return value

	# connection.close()

	if format_ == "csv":
		pass
		# return download csv file
	else:
		appointyears = [x for x in range(2018, 2010, -1)]
		appointparties = ['Republican', 'Democrat', 'Other']
		appointgenders = ['Female', 'Male', 'Other']
		return flask.render_template('appoints.html', appointyears=appointyears, appointparties=appointparties, appointgenders=appointgenders)

@app.route('/bills')
def bills():
	format_ = request.args.get("format", None)
	bill = request.args.get("name", "")
	billdate = request.args.get("billdate", "")
	billparty = request.args.get("billparty", "")
	billlocation = request.args.get("billlocation", "")

	# 1. Assign variable to database
	# 2. (Maybe?) Use dictionary function
	# 3. (Maybe?) Cursor variable
	# 4. Create string for SQL command with unknowns
	# 5. Initialize empty strings for SQL command

	if bill:
		pass
		# Change empty string command (#5)

	# Use % to complete SQL command (with limit statement)

	if bill:
		pass
		# Execute the command using cursor.execute
	else:
		pass
		# Execute without the specified query (drop-downs only)
	# Assign variable for return value

	# connection.close()

	if format_ == "csv":
		pass
		# return download csv file
	else:
		billyears = [x for x in range(2018, 2010, -1)]
		billparties = ['Republican', 'Democrat', 'Other']
		billlocation = ['Sacramento', 'Other']
		return flask.render_template('bills.html', billyears=billyears, billparties=billparties, billlocation=billlocation)

@app.route('/press')
def press():
	format_ = request.args.get("format", None)
	location = request.args.get("name", "")
	year = request.args.get("year", "")
	category = request.args.get("category", "")

	# 1. Assign variable to database
	# 2. (Maybe?) Use dictionary function
	# 3. (Maybe?) Cursor variable
	# 4. Create string for SQL command with unknowns
	# 5. Initialize empty strings for SQL command

	# Use % to complete SQL command (with limit statement)

	# Execute without the specified query (drop-downs only)
	
	# Assign variable for return value

	# connection.close()

	if format_ == "csv":
		pass
		# return download csv file
	else:
		years = [x for x in range(2018, 2010, -1)]
		categories = ['appointments', 'veterans-military', 'media-advisories', 'Other']
		locations = ['Sacramento', 'Other']
		return flask.render_template('press.html', locations=locations, categories=categories, years=years)
 
@app.route('/speakers')
def speakers():
	"""
	This is how arguments are passed from the View to this controller
	The get request can look like this: 
	/speakers?name=rubio&format=csv
	This tells the controller to get all speeches by rubio in a csv format
	/speakers?name=rubio
	the url above just tells the controller to get speeches by rubio and display them
	/speakers
	The url above simply asks for all speeches to be displayed
	/speakers?format=csv
	Asks for all speeches to be made available in csv format
	"""

	format_ = request.args.get("format", None)
	speaker = request.args.get("name", "")

	connection = sqlite3.connect("mydatabase.sqlite") 
	connection.row_factory = dictionary_factory
	cursor = connection.cursor()

	#Query that gets the records that match the query
	all_records_query = "SELECT hearing.hearing_title as title, hearing.date as date, speech.text as text, \
				speaker.surname as name FROM hearing inner join speech on \
				speech.hearing_id = hearing.hearing_id inner join speaker \
				on speaker.speech_id = speech.speech_id %s %s;"

	where_clause = ""
	if speaker:
		where_clause = "where speaker.surname = ? " if speaker else ""

	limit_statement = "limit 20" if format_ != "csv" else ""

	all_records_query = all_records_query % (where_clause, limit_statement)

	if speaker:
		cursor.execute(all_records_query ,(speaker.lower(),))
	else:
		cursor.execute(all_records_query)
	records = cursor.fetchall()

	connection.close()

	#Send the information back to the view
	#if the user specified csv send the data as a file for download else visualize the data on the web page
	if format_ == "csv": 
		return download_csv(records, "speeches_%s.csv" % (speaker.lower()))
	else:
		years = [x for x in range(2018, 1995, -1)]
		return flask.render_template('speaker.html', records=records, speaker=speaker, years=years)

########################################################################
# The following are helper functions. They do not have a @app.route decorator
########################################################################
def dictionary_factory(cursor, row):
	"""
	This function converts what we get back from the database to a dictionary
	"""
	d = {}
	for index, col in enumerate(cursor.description):
		d[col[0]] = row[index]
	return d

def download_csv(data, filename):
	"""
	Pass into this function, the data dictionary and the name of the file and it will create the csv file and send it to the view
	"""
	header = data[0].keys() #Data must have at least one record.
	with open('downloads/' + filename, "w+") as f:
		writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		writer.writerow(header)
		for row in data:
			writer.writerow(list(row.values()))
	
	#Push the file to the view
	return send_file('downloads/' + filename,
				 mimetype='text/csv',
				 attachment_filename=filename,
				 as_attachment=True)


if __name__ == '__main__':
	app.debug=True
	app.run()
