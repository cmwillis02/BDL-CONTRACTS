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
			"SELECT week_id, year, week FROM week_dim WHERE week_id IN (SELECT min(week_id) FROM week_dim WHERE run_status <> 1)"
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

 
 
 
        
def create_mfl_json(server, year, week, league_id):
    
    url = 'http://www' + str(server) + '.myfantasyleague.com/' + str(year) + '/export?TYPE=playerScores&L=' + str(league_id) + '&W=' + str(week) + '&YEAR=' + str(year) + '&PLAYERS=&POSITION=&STATUS=&RULES=&COUNT=&JSON=1'
    print (url)
    
    uh= urlopen(url)
    data= uh.read()
    js= json.loads(data)
    
    return js
    
def import_player_scores(server, year, week, league_id, week_id):
    
    js=create_mfl_json(server, year, week, league_id)
    for item in js["playerScores"]["playerScore"]:
        
        status='FA'
        score = item["score"]
        player_id = item["id"]
        
        cur.execute(
        			"INSERT INTO player_fact (player_id, week_id, roster_status, actual_status, score) VALUES (%s, %s, %s, %s, %s)", (player_id, week_id, 'FA', 'Active', score)
        			)

        
        
        

import_player_scores(server, year , week , league_id, week_id)
conn.commit()

cur.execute(
			"UPDATE week_dim SET run_status = 1 WHERE week_id = %s", (week_id, )
			)

conn.commit()
