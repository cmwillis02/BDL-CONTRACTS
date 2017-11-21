import requests

class _import():
	
	def __init__(self):
		
		self.league_id= 69302
		self.username= "cmwillis02"
		self.password= "02guam04"
		self.year= 2017
		self.proto= "https://"
		self.host= "www61.myfantasyleague.com/"
		self.import_url= "{}{}/{}/import".format(self.proto, self.host, self.year)
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
