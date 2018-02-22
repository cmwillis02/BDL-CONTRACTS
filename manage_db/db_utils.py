#!/usr/bin/python3.6

import MySQLdb as sqldb
import sys

class db_util():

	def __init__(self):
		
		db=sqldb.connect(
						host="localhost",
						user="root",
						passwd="Bdladmin!23",
						db="BDLCORE")
		
		self.cur= db.cursor()

			
	def get_current_week(self):
		
		self.cur.execute("SELECT week_id, year, week FROM contracts_week WHERE run_status= 0 AND week_id= (SELECT min(week_id) FROM contracts_week WHERE run_status= 0)")
		return self.cur.fetchall()[0]
		