#!/usr/bin/python3.6

import MySQLdb as sqldb
import json
import sys
import time
import datetime
try:
	import mfl_api
except:
	from manage_db import mfl_api
    
class contract_process(object):

	def __init__(self, roster_json):
		
		try:
			db=sqldb.connect(
							host="localhost",
							user="root",
							passwd="Bdladmin!23",
							db="BDLCORE")
			self.cur= db.cursor()
			print ('connected')
			
		except:
			print ('Failed to connect')

			
		# Lists used to close contracts that are not new or recently processed
		self.cur.execute(
				'SELECT player_id, franchise_id, id FROM contracts_contract WHERE current_ind = true'
				)
		
		self.starting_contracts = self.cur.fetchall()
		self.processed_contracts= []
		self.roster_json= roster_json
		
	def main_process(self):

		for franchise in range(0,10):
			
			franchise_id= franchise + 1
			for item in self.roster_json["rosters"]["franchise"][franchise]["player"]:

				player_id= item['id']
				years= item['contractYear']
				if item['status'] == "INJURED_RESERVE":
					ir= 'i'
				else:
					ir= 'a'
					
				status= self.set_status(player_id, franchise_id)

				if status[0]== 'new':
					self.new_contract(player_id, franchise_id, 0, ir)
				elif status[0]== 'current':
					self.set_ir(ir, status[1])
					self.processed_contracts.append(status[1])
				elif status[0]== 'edit':
					self.close_contract(status[1])
					self.new_contract(player_id, franchise_id, years, ir)
					
		self.close_remaining()
		self.auto_assign()	
		self.conn.commit()
		
	def close_remaining(self):

		for contract in self.starting_contracts:
			if contract[2] in self.processed_contracts:
				continue
			else:
				print (contract[2])
				self.close_contract(contract[2])
				
	def auto_assign(self):
		
		self.cur.execute(
				"SELECT id, player_id FROM contracts_contract WHERE current_ind = 'true' AND years = 0"
				)
		results= self.cur.fetchall()
		
		for row in results:
			mfl_obj= mfl_api.export()
			status= mfl_obj.game_status(row[1])

			if status == 'unlocked':
				continue
			else:
				self.cur.execute(
							"UPDATE contracts_contract SET years= 1, years_remaining= 1 WHERE id= %s",(row[0],)
							)
	
		
								
	# --- INDIVIDUAL CONTRACT METHODS ---#
	def set_status(self, player_id, franchise_id):
	
		self.cur.execute(
						"SELECT id FROM contracts_contract WHERE player_id= %s AND franchise_id= %s AND current_ind= 'Y'",(player_id, franchise_id)
						)
		result= self.cur.fetchone()
						
		if result is None:
			self.cur.execute(
							"SELECT id FROM contracts_contract WHERE player_id= %s AND current_ind= 'Y'", (player_id,)
							)
			result= self.cur.fetchone()
			if result is None:
				status= 'new'
				id= None
			else:
				status= 'edit'
				id= result[0]
		else:
			status= 'current'
			id= result[0]

		return (status, id)
		
	def new_contract(self, player_id, franchise_id, years, ir):
	
		self.cur.execute(
						"INSERT INTO contracts_contract (current_ind, roster_status, date_assigned, franchise_id, player_id, years, years_remaining) VALUES (%s, %s, %s, %s, %s, %s, %s)", (True, ir, datetime.date.today(), franchise_id, player_id, years, years)
						)
		self.cur.execute(
						"SELECT max(id) FROM contracts_contract"
						)
		id= self.cur.fetchone()[0]
		self.processed_contracts.append(id)
						
	def set_ir(self, ir, id):
		
		self.cur.execute(
						"UPDATE contracts_contract SET roster_status = %s WHERE id= %s",(ir, id)
						)
						
	def close_contract(self, contract_id):
		
		today= datetime.date.today()
		self.cur.execute(
						"UPDATE contracts_contract SET current_ind = 'false', date_terminated= %s, years_remaining= %s, roster_status= %s WHERE id= %s",(today, None, None, contract_id)
						)
