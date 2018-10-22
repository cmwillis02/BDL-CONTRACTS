import csv
import logging
import sys

import MySQLdb as sqldb

import connect_db as conn

FILENAME= 'RFA_players_2018.csv'

class db_util(conn.Connect):

	def export_contracts(self):
		self.connect()
		
		self.cur.execute(
							"SELECT p.player_id, p.name, c.years_remaining,f.team_name FROM contracts_contract c LEFT JOIN contracts_player p on (p.player_id = c.player_id) LEFT JOIN contracts_franchise f ON (f.franchise_id = c.franchise_id) WHERE c.current_ind = 1 and c.years_remaining= 0;"
							)
		results= self.cur.fetchall()
		
		
		with open(FILENAME, 'w') as f:
			writer= csv.writer(f)
			writer.writerow(('Name','Years', 'Team'))
			writer.writerows(results)
		
	
if __name__ == '__main__':
	
	obj= db_util()
	obj.export_contracts()