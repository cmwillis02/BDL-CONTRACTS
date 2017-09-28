import psycopg2
from urllib.request import urlopen
import json
import sys
import datetime



# -- DATABASE DEFINITIONS -- #
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
				'SELECT player_id, franchise_id FROM contracts_contract WHERE current_ind = true'
				)
	current_contracts = cur.fetchall()
	return current_contracts


class contract(object):
	"""
	Class for processing incomming contracts, 3 methods (New Contract, Change Contract, Close Contract)
	"""
	
	
	def __init__(self, player_id, franchise_id, years):
	
		self.player_id= player_id
		self.franchise_id= franchise_id
		self.years= years
		self.status= ''
		self.current_contract_id= None
		
	def set_status(self):
	
		# Set status = 'Current or 'Edit'
		for player_id, franchise_id in current_contracts:
			
			if player_id == int(self.player_id):
				if str(franchise_id) == str(self.franchise_id):
					self.status= 'Current'
					break
				
				else:
					self.status= 'Edit'
					
					cur.execute(
								"SELECT id FROM contracts_contract WHERE player_id= %s AND franchise_id= %s AND current_ind = 'Y'", (self.player_id, self.franchise_id)
								)
					self.current_contract_id= cur.fethcall()[0]
					
					break
			
			else:
				self.status= 'New'
		
	def enter_new_contract():

		#cur.execute(
		#			'INSERT INTO contracts_contract (current_ind, date_assigned, franchise_id, player_id, years) VALUES (%s, %s, %s, %s, %s)',('true',datetime.date.today(), self.franchise_id, self.player_id, self.years)
		#			)
		print (player_id, franchise_id, years, 'NEW CONTRACT')
		
	def close_current_contract():
		
		# Close original contract then enter updated contract
		cur.execute(
					"UPDATE contracts_contract SET current_ind = ?, date_terminated = ? WHERE id = ?", ('N', datetime.date.today(), self.current_contract_id)
					)
		conn.commit()
		
def close_contracts(updated_contracts):
	# Close all contracts that are no longer current
	
	for entry in updated_contracts:
		print ([item for item in current_contracts if item[2] == entry])
				


# -- MAIN PROCESS -- #


current_contracts= get_current_contracts()
updated_contracts= []

rosters_js= create_json(61,'rosters', 2017, 21676)
for franchise in range(0,10):
		
	franchise_id= franchise + 1
	for item in rosters_js["rosters"]["franchise"][franchise]["player"]:
		
		player_id= item['id']
		years= item['contractYear']
		
		contract_entry= contract(player_id, franchise_id, years)
		contract_entry.set_status()
		
		if contract_entry.status == 'Current': continue
		
		elif contract_entry.status == 'New':
			contract_entry.enter_new_contract()
		
		elif contract_entry.status == 'Edit':
			contract_entry.close_current_contract()
			contract_entry.enter_new_contract()
			
		updated_contracts.append(contract_entry.current_contract_id)
			
		
				