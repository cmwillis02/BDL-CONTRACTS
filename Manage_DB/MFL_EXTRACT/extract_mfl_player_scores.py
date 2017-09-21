import sqlite3
import urllib2
import json

path='C:\Users\cwillis\Desktop\BDL v3.0\Data\Landing\ETL_MFL_RAW.sqlite'

conn = sqlite3.connect(path)
cur = conn.cursor()

def initialize_db():


    cur.execute('''DROP TABLE IF EXISTS playerscores ''')
    cur.execute('''CREATE TABLE playerscores (  player_id TEXT,
                                                year INTEGER,
                                                week INTEGER,
                                                score REAL,
                                                status TEXT)''')
        
def create_mfl_json(server, year, week, league_id):
    
    url = 'http://www' + str(server) + '.myfantasyleague.com/' + str(year) + '/export?TYPE=playerScores&L=' + str(league_id) + '&W=' + str(week) + '&YEAR=' + str(year) + '&PLAYERS=&POSITION=&STATUS=&RULES=&COUNT=&JSON=1'
    uh = urllib2.urlopen(url)
    data = uh.read()
    js=json.loads(str(data))
    
    return js
    
def import_player_scores(server, year, week, league_id):
    
    js=create_mfl_json(server, year, week, league_id)
    for item in js["playerScores"]["playerScore"]:
        
        print item
        status='FA'
        score = item["score"]
        player_id = item["id"]
        
        print player_id, score, status, year, week
        
        cur.execute('''INSERT INTO playerscores (player_id, year, week, score, status) VALUES (?,?,?,?,?)''',(player_id, year, week, score, status))
    conn.commit()
        
def run_process(server, year, league_id):
    for week in range(1,2):
        import_player_scores(server, year, week, league_id)

initialize_db()
run_process(61, 2017, 21676)

