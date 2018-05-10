#!/usr/bin/python3.6

import MySQLdb as sqldb
import sys
from . import connect_db as conn

class db_util(conn.Connect):
			
	def get_current_week(self):
		
		self.connect()
		self.cur.execute("SELECT week_id, year, week FROM contracts_week WHERE run_status= 0 AND week_id= (SELECT min(week_id) FROM contracts_week WHERE run_status= 0)")
		results= self.cur.fetchall()[0]
		return results
		
	def get_mfl_connection(self, year):
		
		year= self.get_current_week()[1]
		self.cur.execute(
						"SELECT league_id, url FROM url_reference WHERE year = %s",(year,)
						)
		results= self.cur.fetchall()[0]
		return results
		
	def get_job_list(self, week):	
		
		self.cur.execute(
						"SELECT jc.job_id, jd.job_name FROM job_calendar jc LEFT JOIN job_dim jd ON (jd.job_id = jc.job_id) WHERE jc.week= %s AND jd.active_flg= 1",(week, )
						)
		job_list= [i for i in self.cur.fetchall()]				
		
		return (job_list)
		
	def close_week(self):
		
		week= self.get_current_week()[0]
		
		self.cur.execute(
						"UPDATE contracts_week SET run_status = 1 WHERE week_id= %s",(week,)
						)
		self.commit("CLOSE WEEK {}".format(week))
		
		