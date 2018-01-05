#!/usr/bin/python3.6

import psycopg2
import sys
import datetime


class Manage_weeks(object):

	def __init__(self):
		
		
		# DB connection parameters
		self.dsn_database= 'CORE'
		self.dsn_hostname= 'bdlcompanion.cquxuyvkuxqs.us-east-1.rds.amazonaws.com'
		self.dsn_port = '5432'
		self.dsn_uid= 'bdladmin'
		self.dsn_pwd= 'bdladmin!23'
		
		# DB connection
		try:
			conn_string= "host={} port={} dbname={} user={} password= {}".format(self.dsn_hostname, self.dsn_port, self.dsn_database, self.dsn_uid, self.dsn_pwd)
			self.conn=psycopg2.connect(conn_string)
			
			self.cur= self.conn.cursor()
		except:
			print ('Unable to Connect')
			sys.exit(1)
			
	def add_week(self, year, week, start_date, end_date):
		
		week_id= int(str(year) + str(week))
		start_date= datetime.date(int(start_date[0]), int(start_date[1]), int(start_date[2]))
		end_date= datetime.date(int(end_date[0]), int(end_date[1]), int(end_date[2]))
		
		self.cur.execute(
							"INSERT INTO contracts_week (week_id, year, week, start_date, end_date, run_status) VALUES (%s, %s, %s, %s, %s, %s)",(week_id, year, week, start_date, end_date, 0)
						)
						
		self.conn.commit()
		


# Add a week (Year, Week, tuple(Y,M,D), tuple(Y,M,D))

week_obj= Manage_weeks()
week_obj.add_week(2018, 99, ('2018','01','02'), ('2018','09','01'))