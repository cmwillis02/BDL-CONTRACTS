#!/usr/bin/python3.6

import psycopg2
from urllib.request import urlopen
import json
import sys
import time
import datetime
from manage_db import mfl_api



# -- DATABASE DEFINITIONS AND CURSOR CONNECTION -- #
dsn_database= 'CORE'
dsn_hostname= 'bdlcompanion.cquxuyvkuxqs.us-east-1.rds.amazonaws.com'
dsn_port = '5432'
dsn_uid= 'bdladmin'
dsn_pwd= 'bdladmin!23'

try:
	conn_string= "host=" + dsn_hostname + " port=" + dsn_port+" dbname=" + dsn_database + " user=" + dsn_uid + " password=" + dsn_pwd
	conn= psycopg2.connect(conn_string)
	cur= conn.cursor()
	print ('Connected')
except:
	print ('Unable to connect')
	sys.exit(1)


# -- FUNCTION AND CLASS DEFINITIONS -- #

def create_json(server,type, year, league_id):

	url= 'http://www' + str(server) + '.myfantasyleague.com/' + str(year) + '/export?TYPE=' + type + '&L=' + str(league_id) + '&APIKEY=&FRANCHISE=&JSON=1'

	uh= urlopen(url)
	data= uh.read()
	js=json.loads(data)

	return js

def get_current_contracts():
	#Create list of players with a current contract

	cur.execute(
				'SELECT player_id, franchise_id, id FROM contracts_contract WHERE current_ind = true'
				)
	current_contracts = cur.fetchall()
	return current_contracts

def close_current_contract(contract_id):
		# Close a contract with current_ind = 'Y'

		cur.execute(
					"UPDATE contracts_contract SET current_ind = %s, date_terminated = %s, years_remaining= 0, roster_status= '' WHERE id = %s", ('N', datetime.date.today(), contract_id)
					)

def close_remaining_contracts(current_contracts, processed_contracts):
	# Close all contracts that are no longer current

	for player, franchise, id in current_contracts:

		if id not in processed_contracts:
			close_current_contract(id)

def auto_assign():
	
	cur.execute(
				"SELECT id, player_id FROM contracts_contract WHERE current_ind = 'true' AND years = 0"
				)
	results= cur.fetchall()
	
	for row in results:
		mfl_obj= mfl_api.export()
		status= mfl_obj.game_status(row[1])
		
		if status == 'unlocked':
			continue
		else:
			cur.execute(
						"UPDATE contracts_contract SET years= 1, years_remaining= 1 WHERE id= %s",(row[0])
						)



class contract(object):
	"""
	Class for processing incomming contracts method to set the status, enter the information as a new contract, and update the processed contract list.
	"""


	def __init__(self, player_id, franchise_id, years, ir):

		self.player_id= player_id
		self.franchise_id= franchise_id
		self.years= years
		self.status= ''
		self.current_contract_id= None
		self.ir= ir

	def set_status(self):

		# Set status = 'Current or 'Edit'
		for player_id, franchise_id, id in current_contracts:

			if player_id == int(self.player_id):
				if str(franchise_id) == str(self.franchise_id):
					self.status= 'Current'

					cur.execute(
								"SELECT id FROM contracts_contract WHERE player_id= %s AND franchise_id= %s AND current_ind = 'Y'", (self.player_id, self.franchise_id)
								)
					self.current_contract_id= cur.fetchone()[0]

					break

				else:
					self.status= 'Edit'

					cur.execute(
								"SELECT id FROM contracts_contract WHERE player_id= %s AND current_ind = 'Y'", (self.player_id,)
								)
					self.current_contract_id= cur.fetchone()[0]

					break

			else:
				self.status= 'New'


	def enter_new_contract(self):

		# All new contracts should be default assigned to 0 years by MFL.  This will allow traded contracts not to show up on pending assignment
		if self.status == 'New':
			self.years= 0
		
		cur.execute(
					'INSERT INTO contracts_contract (current_ind, roster_status, date_assigned, franchise_id, player_id, years, years_remaining) VALUES (%s, %s, %s, %s, %s, %s, %s)',('true', ir, datetime.date.today(), self.franchise_id, self.player_id, self.years, self.years)
					)


	def update_processed_contract_list(self):
		# Create a list of contract IDs that are still current, this will be used to close conctract IDs that are no longer valid.

		if self.current_contract_id != None:
			processed_contracts.append(self.current_contract_id)
			
	def set_ir(self):
		#Check and set IR status (i= IR, a= ACTIVE)
		
		cur.execute(
					"UPDATE contracts_contract SET roster_status = %s WHERE id = %s",(self.ir, self.current_contract_id)
					)
		





# -- MAIN PROCESS -- #

# -- Create lists of contracts currently in the database (current_contracts) and the empty list of contracts to be processed from MFL (processed_contracts)
current_contracts= get_current_contracts()
processed_contracts= []

# -- Capture JSON of current MFL Roster
rosters_js= create_json(61,'rosters', 2017, 21676)
for franchise in range(0,10):

	franchise_id= franchise + 1
	for item in rosters_js["rosters"]["franchise"][franchise]["player"]:

		player_id= item['id']
		years= item['contractYear']
		if item['status'] == "INJURED_RESERVE":
			ir= 'i'
		else:
			ir= 'a'

		# -- Create contract object for each contract entry and determine the status (Current, Edit, New)
		contract_entry= contract(player_id, franchise_id, years, ir)
		contract_entry.set_status()

		# -- Process each contract entry according to status
		if contract_entry.status == 'Current':
			
			contract_entry.set_ir()
			contract_entry.update_processed_contract_list()

		elif contract_entry.status == 'New':
			contract_entry.enter_new_contract()

			contract_entry.update_processed_contract_list()

		elif contract_entry.status == 'Edit':
			close_current_contract(contract_entry.current_contract_id)
			contract_entry.enter_new_contract()

			contract_entry.update_processed_contract_list()

close_remaining_contracts(current_contracts, processed_contracts)
# Auto assign contracts to 1 year if players game has started
auto_assign()
conn.commit()

# Update job_log table
cur.execute(
				'INSERT INTO job_log (job_name, run_date) VALUES (%s, %s)',('Update Rosters', int(time.time()))
				)
conn.commit()

