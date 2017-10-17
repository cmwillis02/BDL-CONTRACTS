#!/usr/bin/python

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

	run_date= ''
	
	url= 'http://www' + str(server) + '.myfantasyleague.com/' + str(year) + '/export?TYPE=' + type + '&L=' + str(league_id) + '&SINCE=' + run_date + '&APIKEY=&FRANCHISE=&JSON=1'

	print (url)
	uh= urlopen(url)
	data= uh.read()
	js=json.loads(data)
	
	return js



def load_players(url, year, league_id):
	
	players_js= create_json(url,'players',year , league_id)
	
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
			
			
			
			try:
				cur.execute(
							'INSERT INTO contracts_player (player_id, position, name) VALUES (%s, %s, %s)',(player_id, position_code, name)
							)
				conn.commit()
				print (name, position)
				
			except psycopg2.IntegrityError:
				conn.rollback()


load_players(61, 2017, 21676)
load_players(56, 2016, 21676)
load_players(56, 2015, 37270)
load_players(56, 2014, 22529)
load_players(63, 2013, 34909)
load_players(65, 2012, 40396)
load_players(54, 2011, 18198)
load_players(59, 2010, 46342)
load_players(55, 2009, 52094)
			






