import requests
import json
from manage_db import db_utils

class _import():
	
	def __init__(self):
		
		week_data= db_utils.db_util()
		
		self.league_id= 69302
		self.username= "cmwillis02"
		self.password= "02guam04"
		self.year= week_data.get_current_week()[1]
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
		
	def import_message_board(self, thread, body, type):
		"""
		Deliver message board post to MFL, use type= new to post new thread and type= current to post a new message to a current thread
		"""
		
		req_type= "messageBoard"
		self.login()
		
		if type == 'new':
			import_url= "{}?TYPE={}&L={}&THREAD=&SUBJECT={}&BODY={}".format(self.import_url, req_type, self.league_id, thread, body)
		elif type== 'current':
			import_url= "{}?TYPE={}&L={}&THREAD={}&SUBJECT=&BODY={}".format(self.import_url, req_type, self.league_id, self.contract_thread_id, body)
		
		r= self.session.post(import_url)

class export():

	def __init__(self):
		
		#DRY these should be read from somewhere
		week_data= db_utils.db_util()
		
		self.league_id= 21676
		self.username= "cmwillis02"
		self.password= "02guam04"
		self.year= week_data.get_current_week()[1]
		self.week= week_data.get_current_week()[2]
		self.proto= "https://"
		self.host= "www61.myfantasyleague.com/"
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
		
		type= "liveScoring"
		url= '{}?TYPE={}&L={}&W={}&DETAILS=1&JSON=1'.format(self.export_url, type, self.league_id, self.week)
		response= self.session.get(url)
		json_data= json.loads(response.text)
		
		if self.week in [14,15,16]:
			matchups= 2
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
			for team in range(0,6):
				players= json_data['liveScoring']['franchise'][team]['players']['player']
				for player in players:
					if int(player['id']) == player_id:
						if int(player['gameSecondsRemaining']) < 3600:
							status= 'locked'
						else:
							status= 'unlocked'
		
		return status