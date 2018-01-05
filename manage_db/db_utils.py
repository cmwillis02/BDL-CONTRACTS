#!/usr/bin/python3.6

import psycopg2

class db_util():

	def __init__(self):
		
		self.dsn_database= 'CORE'
		self.dsn_hostname= 'bdlcompanion.cquxuyvkuxqs.us-east-1.rds.amazonaws.com'
		self.dsn_port = '5432'
		self.dsn_uid= 'bdladmin'
		self.dsn_pwd= 'bdladmin!23'

	def connect(self):
		
		try:
			conn_string= "host={} port={} dbname={} user={} password={}".format(self.dsn_hostname, self.dsn_port, self.dsn_database, self.dsn_uid, self.dsn_pwd)
			conn= psycopg2.connect(conn_string)
			cur= conn.cursor()
			
			return cur
		
		except:
			print ('Unable to connect')
			sys.exit(1)
			
	def get_current_week(self):
		
		cur= self.connect()
		
		cur.execute("SELECT week_id, year, week FROM contracts_week WHERE run_status= 0 AND week_id= (SELECT min(week_id) FROM contracts_week WHERE run_status= 0)")
		return cur.fetchall()[0]
		