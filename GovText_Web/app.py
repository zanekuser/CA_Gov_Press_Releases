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


	connection = sqlite3.connect("database.db")
	connection.row_factory = dictionary_factory
	cursor = connection.cursor()

	all_records_query = "SELECT post_id AS PostID, name AS Appointee, \
	date AS Year, party AS Party, gender AS Gender, \
	description AS Description FROM appointments %s %s;"


	where_clause = ""
	where_list = []
	condition_tuple = []
	if appointee or appointyear or appointparty or appointgender:
		where_clause += 'where '
		if appointee:
			where_list.append('name like ? ')
			condition_tuple.append('%' + appointee.lower() + '%')

		if appointyear:
			where_list.append('date like ? ')
			condition_tuple.append('%' + str(appointyear))

		if appointparty:
			where_list.append('party == ? ')
			condition_tuple.append(str(appointparty))

		if appointgender:
			where_list.append('gender == ? ')
			if appointgender == 'Male':
				condition_tuple.append('M')
			elif appointgender == 'Female':
				condition_tuple.append('F')
			else:
				condition_tuple.append(appointgender)


		where_clause += 'and '.join(where_list)

		condition_tuple = tuple(condition_tuple)

		limit_statement = 'ORDER BY post_id LIMIT 10' if format_ != 'csv' else ''

		all_records_query = all_records_query % (where_clause, limit_statement)

		if appointee or appointyear or appointparty or appointgender:
			cursor.execute(all_records_query , condition_tuple)
		else:
			cursor.execute(all_records_query)

		records = cursor.fetchall()

		connection.close()
	else:
		records = None

	# Execute without the specified query (drop-downs only)


	if format_ == "csv":
		return download_csv(records, "appointments_%s.csv" % (appointee.lower()))
		# return download csv file
	else:
		appointyears = [x for x in range(2018, 2010, -1)]
		appointparties = ['Republican', 'Democrat', 'Other']
		appointgenders = ['Female', 'Male', 'Other']
		return flask.render_template('appoints.html', records=records, appointyears=appointyears,
									 appointparties=appointparties, appointgenders=appointgenders)

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
	postid = request.args.get("postid", "")
	location = request.args.get("location", "")
	year = request.args.get("year", "")
	month = request.args.get("month", "")

	connection = sqlite3.connect("database.db")
	connection.row_factory = dictionary_factory
	cursor = connection.cursor()

	all_records_query = "SELECT post_id AS PostID, strftime('%%m', date) AS MONTH, \
	strftime('%%Y', date) AS YEAR, location AS LOCATION, \
	title AS TITLE FROM all_releases %s %s;"

	where_clause = ""
	where_list = []
	condition_tuple = []
	if postid or location or year or month:
		where_clause += 'where '
		if postid:
			where_list.append('post_id like ? ')
			condition_tuple.append('%' + postid.lower() + '%')

		if month:
			where_list.append("strftime('%m', date) like ? ")
			condition_tuple.append('%' + str(month))

		if year:
			where_list.append("strftime('%Y', date) like ? ")
			condition_tuple.append('%' + year)

		if location:
			where_list.append('location like ? ')
			condition_tuple.append('%' + location.lower())

		where_clause += 'and '.join(where_list)

		condition_tuple = tuple(condition_tuple)

		limit_statement = 'ORDER BY post_id LIMIT 10' if format_ != 'csv' else ''

		all_records_query = all_records_query % (where_clause, limit_statement)

		if postid or location or year or month:
			cursor.execute(all_records_query , condition_tuple)
		else:
			cursor.execute(all_records_query)

		records = cursor.fetchall()

		connection.close()
	else:
		records = None

	# Execute without the specified query (drop-downs only)

	if format_ == "csv":
		pass
		# return download csv file
	else:
		years = [x for x in range(2018, 2010, -1)]
		months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
		return flask.render_template('press.html', records=records, months=months, years=years)

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
