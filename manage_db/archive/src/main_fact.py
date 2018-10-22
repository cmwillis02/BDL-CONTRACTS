#!/usr/bin/python3.6


import MySQLdb as mysql

from util import connect_db as conn
from util import mfl_api as mfl
from util import db_utils as util


class Fact(conn.Connect):

	def __init__(self, player_scores_json, weekly_results_json, week_id):
	
		self.connect()
		self.player_scores_json= player_scores_json
		self.weekly_results_json= weekly_results_json
		self.results_list= []
		self.matchup_list= []
		self.week_id= week_id
		
		
	def main_process(self):
	
		self.weekly_results()
		self.player_scores()
		self.set_matchups()
		self.commit("Player/Franchise_Fact")
		
	def player_scores(self):
		for item in self.player_scores_json["playerScores"]["playerScore"]:

			status='f'
			score = float(item["score"])
			player_id = item["id"]
			franchise_id= None
			
			for player in self.results_list:
				if player[0] == player_id:
					franchise_id= player[3]
					status= player[1]
					break
			 	
				else:
					continue
			try:
				self.cur.execute(
									"INSERT INTO history_player_fact (player_id, franchise_id, week_id, score, roster_status) VALUES (%s, %s, %s, %s, %s)",(player_id, franchise_id, self.week_id, score, status)
									)
			except (mysql.Error, mysql.Warning) as err:
  				print("player_id= {}, franchise_id= {}, week_id= {} score= {} :: {}".format(player_id, franchise_id, self.week_id, score, err))
			
			
		self.commit()
			 		
	def weekly_results(self):
	
		#Some weeks require fewer than 5 matchup ids, work up from 0 and except: once finished
		for matchup_id in range(0,5):
			try:
				for item in self.weekly_results_json()["weeklyResults"]["matchup"][matchup_id]["franchise"]:
					print (item)
					franchise_id= item["id"]
		
					try:
						result= item["result"].lower()
					except:
						result= 't'
			
					# Process players
					total_score= 0
					players= item["player"]
					for player in players:
						player_id= player["id"]
						if player["status"] == 'starter':
							status= 's'
							total_score= float(total_score) + float(player["score"])
						else:
							status= 'b'

						if player["score"] == '':
							score= 0
						else:
							score= player["score"]
							
						print (player_id, status, score, franchise_id)
							
						self.results_list.append((player_id, status, score, franchise_id))
					
					print (matchup_id, franchise_id, result, total_score)	
					self.matchup_list.append((matchup_id, franchise_id, result, total_score))
			except:
				break
				
			
				
	def set_matchups(self):
		print (self.matchup_list)
		
		for team in self.matchup_list:
			m_id= team[0]
			franchise_id= team[1]
			result= team[2]
			total_score= team[3]
			matchup_type = 'r'

			for team2 in self.matchup_list:
				if team2[0] == m_id and team2[1] != franchise_id:
					opponent_id= team2[1]
					opponent_score= team2[3]
				else:
					continue
			
			self.cur.execute(
								"INSERT INTO history_franchise_fact (week_id, franchise_id, total_score, result, opponent_id, opponent_score, matchup_type) VALUES (%s, %s, %s, %s, %s, %s, %s)",(self.week_id, franchise_id, total_score, result, opponent_id, opponent_score, matchup_type) 
							)
			self.commit()
							
if __name__ == "__main__":
	api= mfl.export()
		
	#Create Fact class
	process= Fact(api.player_scores(), api.weekly_results, util.get_current_week()[0])
	process.main_process()
	
		