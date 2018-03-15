import requests
import json
from util import db_utils

class _import():

	def __init__(self):
		

		week_data= db_utils.db_util()
		self.year= week_data.get_current_week()[1]
		self.league_id= 69302
		self.username= "cmwillis02"
		self.password= "02guam04"
		self.proto= "https://"
		self.host= "www61.myfantasyleague.com/"
		self.import_url= "{}{}/{}/import".format(self.proto, self.host, self.year)
		self.export_url= "{}{}/{}/export".format(self.proto, self.host, self.year)
		#This needs to be programatic (possibly read from a configuration file
		self.contract_thread_id= 5113555

	def login(self):

		self.session= requests.Session()

		login_url= 'https://api.myfantasyleague.com/{}/login?USERNAME={}&PASSWORD={}&XML=1'.format(self.year, self.username, self.password)
		self.session.get(login_url)

	def import_contract(self, player_id, years):

		req_type= "salaries"
		self.login()

		data= "<salaries><leagueUnit unit='LEAGUE'><player id='{}' contractStatus='Active' contractYear='{}' contractInfo='Imported'/> </leagueUnit></salaries>".format(player_id, years)
		import_url= "{}?TYPE={}&L={}&DATA={}&APPEND=1".format(self.import_url, req_type, self.league_id, data)

		r= self.session.post(import_url)

	def import_message_board(self, message):
		"""
		Deliver message board post to MFL, use type= new to post new thread and type= current to post a new message to a current thread
		"""

		req_type= "messageBoard"
		self.login()

		import_url= "{}?TYPE={}&L={}&THREAD={}&SUBJECT=&BODY={}".format(self.import_url, req_type, self.league_id, self.contract_thread_id, message)

		r= self.session.post(import_url)

class export():

	def __init__(self):

		util_data= db_utils.db_util()
		self.year= util_data.get_current_week()[1]
		self.week= util_data.get_current_week()[2]		
		self.league_id= util_data.get_mfl_connection(self.year)[0]
		self.username= "cmwillis02"
		self.password= "02guam04"
		self.proto= "https://"
		self.host= "www{}.myfantasyleague.com/".format(util_data.get_mfl_connection(self.year)[1])
		self.export_url= "{}{}{}/export".format(self.proto, self.host, self.year)
		

	def login(self):

		self.session= requests.Session()

		login_url= 'https://api.myfantasyleague.com/{}/login?USERNAME={}&PASSWORD={}&XML=1'.format(self.year, self.username, self.password)
		self.session.get(login_url)
		

	def player_status(self, player_id):

		self.login()

		type= "playerStatus"
		url= '{}?TYPE={}&L={}&P={}&JSON=1'.format(self.export_url, type, self.league_id, player_id)
		response= self.session.get(url)
		json_data= json.loads(response.text)

		return json_data

	def game_status(self, player_id):

		self.login()
		
		if self.week == 99:
			status= 'locked'

		else:
			type= "liveScoring"
			url= '{}?TYPE={}&L={}&W={}&DETAILS=1&JSON=1'.format(self.export_url, type, self.league_id, self.week)
			response= self.session.get(url)
			json_data= json.loads(response.text)
			
			if self.week == 14:
				matchups= 4
			elif self.week == 15:
				matchups= 3
			elif self.week == 16:
				matchups= 2
			elif self.week == 17:
				matchups= 0
			else:
				matchups= 5

			for matchup in range(0,matchups):
				game= json_data['liveScoring']['matchup'][matchup]['franchise']
				for team in range(0,2):
					players= game[team]['players']['player']
					for player in players:
						if int(player['id']) == player_id:
							if int(player['gameSecondsRemaining']) < 3600:
								status= 'locked'
							else:
								status= 'unlocked'
							
			if self.week in [14,15,16]:
				teams= 10-(matchups * 2)
				for team in range(0,teams):
					players= json_data['liveScoring']['franchise'][team]['players']['player']
					for player in players:
						if int(player['id']) == player_id:
							if int(player['gameSecondsRemaining']) < 3600:
								status= 'locked'
							else:
								status= 'unlocked'
							
			if self.week == 17:
				status= 'locked'
		
		return status
        
	def rosters(self):
	
		self.login()
		
		type= 'rosters'
		
		url='{}?TYPE={}&L={}&APIKEY=&FRANCHISE=&JSON=1'.format(self.export_url, type, self.league_id)
		response= self.session.get(url)
		json_data= json.loads(response.text)
		print (url)
		
        
		return json_data
		
	def transactions(self):
	
		pass
	
# 		self.login()
# 		
# 		type= 'transactions'
# 		days= 365
# 		trans_type= 'WAIVER'
# 		week= 10
# 		
# 		url= '{}?TYPE={}&L={}&APIKEY=&W={}TRANS_TYPE={}&FRANCHISE=&DAYS={}&COUNT=&JSON=1'.format(self.export_url, self.league_id, week, type, trans_type, days)
	
	def player_dim(self):
		
		self.login()
		type= 'players'
		
		url= '{}?TYPE={}&L={}&SINCE=&APIKEY=&FRANCHISE=&JSON=1'.format(self.export_url, type, self.league_id)
		print (url)
		response= self.session.get(url)
		json_data= json.loads(response.text)
		
		return json_data
		
	def player_scores(self):
		
		self.login()
		type= 'playerScores'
		
		url= '{}?TYPE={}&L={}&W={}&YEAR=&PLAYERS=&POSITION=&STATUS=&RULES=&COUNT=&JSON=1'.format(self.export_url, type, self.league_id, self.week)
		print (url)
		
		response= self.session.get(url)
		json_data= json.loads(response.text)
		
		return json_data
		
	def weekly_results(self):
	
		self.login()
		type= 'weeklyResults'
		
		url= '{}?TYPE={}&L={}&W={}&YEAR=&PLAYERS=&POSITION=&STATUS=&RULES=&COUNT=&JSON=1'.format(self.export_url, type, self.league_id, self.week)
		
		response= self.session.get(url)
		json_data= json.loads(response.text)
		
		return json_data

		