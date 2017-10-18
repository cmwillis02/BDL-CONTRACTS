import psycopg2
from urllib.request import urlopen
import json

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
 
cur.execute(
			"SELECT week_id, year, week FROM contracts_week WHERE week_id IN (SELECT min(week_id) FROM contracts_week WHERE run_status <> 1)"
			)
run_week= cur.fetchall()
week_id= run_week[0][0]
year= run_week[0][1]
week= run_week[0][2]

cur.execute(
			"SELECT url, league_id FROM url WHERE year = %s", (year,)
			)
result= cur.fetchall()
server= str(int(result[0][0]))
league_id = str(int(result[0][1]))

 
 
 
        
def create_mfl_json(server, year, week, league_id, type):
    
    url = 'http://www' + str(server) + '.myfantasyleague.com/' + str(year) + '/export?TYPE=' + type + '&L=' + str(league_id) + '&W=' + str(week) + '&YEAR=' + str(year) + '&PLAYERS=&POSITION=&STATUS=&RULES=&COUNT=&JSON=1'
    print (url)
    print (year, week, type)
    
    uh= urlopen(url)
    data= uh.read()
    js= json.loads(data)
    
    return js
    
def import_player_scores(server, year, week, league_id, week_id):
    
    js=create_mfl_json(server, year, week, league_id, 'playerScores')
    for item in js["playerScores"]["playerScore"]:
        
        status='f'
        score = float(item["score"])
        player_id = item["id"]
        
        cur.execute(
        			"INSERT INTO contracts_player_fact (player_id, week_id, roster_status, score) VALUES (%s, %s, %s, %s)", (player_id, week_id, 'FA',  score)
        			)
        			
def weekly_results_players(players, year, week, franchise_id, m_id, result):

	for player in players:
		player_id= player["id"]
		if player["score"] == '':
			score= 0
		else:
			score= float(player["score"])
		if player["status"] == 'starter':
			status= 's' 
		else: 
			status= 'b'
        
		cur.execute(
					"UPDATE contracts_player_fact SET franchise_id = %s, roster_status = %s WHERE player_id = %s AND week_id = %s", (int(franchise_id), status, player_id, week_id)
					)
		conn.commit()

def import_weekly_results(server, year, week, league_id):
    
	js=create_mfl_json(server, year, week, league_id, 'weeklyResults')

	if year!=2013:

		if week==14:
			r=range(0,4)
		elif week==15:
			r=range(0,3)
		elif week==16:
			r=range(0,2)
		else:
			r=range(0,5)

	else:
		if week==14:
			r=range(0,2)
		elif week==15:
			r=range(0,2)
		elif week==16:
			r=range(0,2)
		else:
			r=range(0,5)

	for m_id in r:
        
		for item in js["weeklyResults"]["matchup"][m_id]["franchise"]:
			franchise_id= item["id"]
			try:
				result= item["result"]
			except:
				result= 't'
			players=item["player"]

			weekly_results_players(players, year, week, franchise_id, m_id, result)
			
			cur.execute(
						"SELECT sum(score) FROM contracts_player_fact WHERE week_id = %s AND franchise_id = %s AND roster_status = 's'", (week_id, franchise_id)
						)
			score= cur.fetchone()[0]
			
			cur.execute(
						"INSERT INTO contracts_franchise_fact (franchise_id, week_id, result, matchup_type, total_score) VALUES (%s, %s, %s, %s, %s)", (franchise_id, week_id, result.lower(), 'r', score)
						)
			conn.commit()
			
			matchups.append((m_id, int(franchise_id), score))
			
def set_matchups(matchup_list):
	
	print ("Set Matchups")
	for team in matchup_list:
		m_id= team[0]
		team_id= team[1]
		
		for team2 in matchup_list:
			if team2[0] == m_id and team2[1] != team_id:
				opponent_id= team2[1]
				opponent_score= team2[2]
			else:
				continue
		
		cur.execute(
					"UPDATE contracts_franchise_fact SET opponent_id = %s, opponent_score = %s WHERE franchise_id = %s AND week_id = %s", (opponent_id, opponent_score, team_id, week_id)
					)
		conn.commit()
					
		
		
			
			
			
                                        
        
# --- MAIN PROCESS --- #        

matchups= []
import_player_scores(server, year , week , league_id, week_id)
import_weekly_results(server, year, week, league_id)
conn.commit()
set_matchups(matchups)

# Update contracts_week to reflect run status after succesful completion.
cur.execute(
			"UPDATE contracts_week SET run_status = 1 WHERE week_id = %s", (week_id, )
			)
conn.commit()
