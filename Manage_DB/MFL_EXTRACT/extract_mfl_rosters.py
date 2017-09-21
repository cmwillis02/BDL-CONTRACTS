import sqlite3
import urllib2
import json

path='C:\Users\cwillis\Desktop\BDL v3.0\Data\Landing\ETL_MFL_RAW.sqlite'

conn = sqlite3.connect(path)
cur = conn.cursor()

def initialize_db():

    cur.execute('''DELETE FROM rosters''')
    conn.commit()
                                                    

def create_mfl_json(server, year, league_id):
    
    
    url = 'http://www' + str(server) + '.myfantasyleague.com/' + str(year) + '/export?TYPE=rosters&L=' + str(league_id) + '&APIKEY=&FRANCHISE=&JSON=1'
    uh = urllib2.urlopen(url)
    data = uh.read()
    js=json.loads(str(data))
    
    return js
    
def import_rosters(server, year, league_id):
    
    js=create_mfl_json(server, year, league_id)
    for franchise in range(0,10):
        franchise_id = franchise+1
        for item in js["rosters"]["franchise"][franchise]["player"]:
            status=item["status"]
            contract=item["contractYear"]
            player_id = item["id"]

            print player_id, franchise_id, contract, status
        
            cur.execute('''INSERT INTO rosters (player_id, franchise_id, status, contract) VALUES (?,?,?,?)''',(player_id, franchise_id, status, contract))
    conn.commit()
    
initialize_db()
import_rosters(61,2017,21676)