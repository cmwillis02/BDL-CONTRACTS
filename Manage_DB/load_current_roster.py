import psycopg2
from urllib.request import urlopen
import json
import sys
import datetime

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

	
	
def create_json(server,type, year, league_id):

	url= 'http://www' + str(server) + '.myfantasyleague.com/' + str(year) + '/export?TYPE=' + type + '&L=' + str(league_id) + '&APIKEY=&FRANCHISE=&JSON=1'
		
	uh= urlopen(url)
	data= uh.read()
	js=json.loads(data)
	
	return js
	
def re_load_rosters(contract_date_override=None):

	rosters_js= create_json(61,'rosters', 2017, 21676)
	for franchise in range(0,10):
		
		franchise_id= franchise + 1
		for item in rosters_js["rosters"]["franchise"][franchise]["player"]:
			if item["status"] == 'INJURED RESERVE':
				status = 'i'
			else:
				status = 'a'
			years= item["contractYear"]
			player_id = item["id"]
			
			if contract_date_override is None:
				date_assigned= datetime.date.today()
			else:
				date_assigned= contract_date_override

			cur.execute(
						'INSERT INTO contracts_contract (current_ind, date_assigned, franchise_id, player_id, years) VALUES (%s, %s, %s, %s, %s)',(True, date_assigned, franchise_id, player_id, years)
						)
			conn.commit()
			
			
re_load_rosters()			
		
