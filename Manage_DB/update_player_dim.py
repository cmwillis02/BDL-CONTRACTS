#!/usr/bin/python3.6

import psycopg2
from urllib.request import urlopen
import json
import sys
import time


dsn_database= 'CORE'
dsn_hostname= 'bdlcompanion.cquxuyvkuxqs.us-east-1.rds.amazonaws.com'
dsn_port = '5432'
dsn_uid= 'bdladmin'
dsn_pwd= 'bdladmin!23'

position_dict= {
				'QB':'q',
				'RB':'r',
				'WR':'w',
				'TE':'t',
				'PK':'k',
				'Def':'d'
				}


try:
	conn_string= "host=" + dsn_hostname + " port=" + dsn_port+" dbname=" + dsn_database + " user=" + dsn_uid + " password=" + dsn_pwd
	conn= psycopg2.connect(conn_string)
	cur= conn.cursor()
	print ('Connected')
except:
	print ('Unable to connect')
	sys.exit(1)

	
	
def create_json(server,type, year, league_id):

	cur.execute(
				"SELECT max(run_date) FROM job_log WHERE job_name = 'load_players'"
				)
	run_date= str(cur.fetchone()[0])
	
	url= 'http://www' + str(server) + '.myfantasyleague.com/' + str(year) + '/export?TYPE=' + type + '&L=' + str(league_id) + '&SINCE=' + run_date + '&APIKEY=&FRANCHISE=&JSON=1'

	print (url)
	uh= urlopen(url)
	data= uh.read()
	js=json.loads(data)
	
	return js



def load_players():
	
	players_js= create_json(61,'players',2017, 21676)
	
	try:
		players_js['error']
		run= 'n'
		print ('NO NEW PLAYERS')
	except:
		run= 'y'
	
	if run == 'y':
	
		for item in players_js["players"]["player"]:
			player_id= item["id"]
			position= item["position"]
		
			if position not in ['QB','RB','WR','TE','PK','Def']: continue
		
			position_code= position_dict[position]
			name= item["name"]
			
			print (name, position)
			
			try:
				cur.execute(
							'INSERT INTO contracts_player (player_id, position, name) VALUES (%s, %s, %s)',(player_id, position_code, name)
							)
				conn.commit()
	
			except psycopg2.IntegrityError:
				conn.rollback()


load_players()

# Update job_log table
cur.execute(
				'INSERT INTO job_log (job_name, run_date) VALUES (%s, %s)',('load players', int(time.time()))
				)
conn.commit()
			






