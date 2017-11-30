#/usr/bin/python3
#
#
#

import csv
import psycopg2
import os
import configparser
import sys

from monitoring_conf import *

def createQuery(file, metadata_dir):
	tags = dict()
	query = "CREATE TABLE " + file[:-4] + "( "
	for row in csv.reader(open(metadata_dir + file,'rU'), delimiter=";", skipinitialspace=True):
		if tags:
			query += row[1] + " " + row[2] 
			if row[3]:
				query += " " + row[3]
			query += ", "
		else:
			for i, item in enumerate(row):
				if item:
					tags[i] = row[i]
			continue
	query = query[:-2] + " )"
	print ( query )
	return query

def readConfig(sections='all', configFile='prepare_db.conf'):
	try:
		config = configparser.ConfigParser()
		config.read(configFile)
		
	except Exception as e:
		print ("Read configuration is failed: prepare_db.conf")
		print (e)
		sys.exit(10)

	params = dict()
	if (sections == 'all'):
		sections = config.sections()
	for section in sections:
		for key in config[section]:
			if (config[section][key]):
 				params[key] = config[section][key]
	return params


def dbConnection(conf):
	test = False
	if test:
		print ( conf )
	try:
		connect_str = "dbname='" + conf['db_name'] + "' user='" + conf['db_user'] + "' host='" + conf['db_host'] + "' password='" + conf['db_password'] + "'"
		conn = psycopg2.connect(connect_str)
		return conn.cursor()
	except Exception as e:
		print ("Connection to the database is failed.")
		print (e)
		sys.exit(11)


def main():
	conf = readConfig()
	cursor = dbConnection(conf)
	directory = conf['metadata_dir']
	files = os.listdir(directory)
	print ( files )
	
	for file in files:
		query = createQuery(file, directory)
		cursor.execute(query)

	#kontrola
	cursor.execute("""SELECT table_schema || '.' ||table_name FROM information_schema.tables WHERE table_schema NOT IN ('pg_catalog','information_schema');""")
	rows = cursor.fetchall()
	if len(rows) == len(files):
		print(rows)
		print ( 'OK' )
	else:
		print ( 'ERROR: Zkontroluj vytvorene tabulky!' )
		for row in rows:
			print(row)
		sys.exit(12)


if __name__ == "__main__":
	main()
