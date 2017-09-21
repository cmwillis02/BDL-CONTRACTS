import sqlite3
import urllib2
import json

path='C:\Users\cwillis\Desktop\BDL v3.0\Data\Landing\ETL_MFL_RAW.sqlite'

conn = sqlite3.connect(path)
cur = conn.cursor()

def initialize_db():
  
    cur.execute('''DROP TABLE IF EXISTS leaguestandings  ''')
    cur.execute('''CREATE TABLE leaguestandings (  franchise_id INTEGER PRIMARY KEY UNIQUE,
                                                    wins INTEGER,
                                                    losses INTEGER,
                                                    ties INTEGER,
                                                    bones INTEGER)''')
                                                    

def create_mfl_json(server, year, league_id):
    
    
    url = 'http://www' + str(server) + '.myfantasyleague.com/' + str(year) + '/export?TYPE=leagueStandings&L=' + str(league_id) + '&APIKEY=&FRANCHISE=&JSON=1'
    uh = urllib2.urlopen(url)
    data = uh.read()
    js=json.loads(str(data))
    
    return js
    
def import_standings(server, year, league_id):
    
    js=create_mfl_json(server, year, league_id)
    
    for item in js["leagueStandings"]["franchise"]:
        franchise_id=item["id"]
        wins=item["h2hw"]
        losses=item["h2hl"]
        ties=item["h2ht"]
        bones=200 - int(item["bbidspent"])
        
        print franchise_id, wins, losses, ties, bones
        
        
        cur.execute('''INSERT INTO leaguestandings (franchise_id, wins, losses, ties, bones) VALUES (?,?,?,?,?)''',(franchise_id, wins, losses, ties, bones))
    conn.commit()
    
initialize_db()
import_standings(61,2017,21676)