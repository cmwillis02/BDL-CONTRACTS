#!/usr/bin/python3.6

import MySQLdb as sqldb
from util import connect_db as conn

class Main_player_dim(conn.Connect):

	def __init__(self, json_data):
		
		self.json_data= json_data
		self.position_dict= {
				'QB':'q',
				'RB':'r',
				'WR':'w',
				'TE':'t',
				'PK':'k',
				'Def':'d'
				}
		self.connect()
	
	def load_players(self):
		
		timestamp= self.json_data["players"]["timestamp"]
		for player in self.json_data["players"]["player"]:
			
			
			position= player["position"]
			
			if position not in ['QB','RB','WR','TE','PK','Def']:
				continue		
			
			position_code= self.position_dict[position]
			player_id= player["id"]
			name= player["name"]
			
			try:
				self.cur.execute(
								"INSERT INTO contracts_player (player_id, position, name) VALUES (%s, %s, %s)",(player_id, position_code, name)
								)
			except:
				self.db.rollback()
				
		self.commit("player_dim")