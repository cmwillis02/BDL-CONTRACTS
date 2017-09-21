import sqlite3
import urllib2
import pandas as pd
import json

path='C:\Users\cwillis\Desktop\BDL v3.0\Data\Landing\ETL_MFL_RAW.sqlite'

conn = sqlite3.connect(path)
cur = conn.cursor()

def initialize_db():

    cur.execute('''DELETE FROM players''')
    

def create_mfl_json(site):
    
    url = site
    uh = urllib2.urlopen(url)
    data = uh.read()
    js=json.loads(str(data))
    
    return js
    
    
def import_players(url):
    
    js=create_mfl_json(url)
    
    for item in js["players"]["player"]:
        
        player_id=item["id"]
        name=item["name"]
        position=item["position"]
        team=item["team"]
        draft_year=item["draft_year"]
        
        try:
            if item["draft_round"] is None:
                draft_round=0
                draft_pick=0
            else:
                draft_round=item["draft_round"]
                draft_pick=item["draft_pick"]
        except:
            draft_round=0
            draft_pick=0
            
        try:
            nfl_id=item["nfl_id"]
        except:
            nfl_id= ''
        
        try:
            espn_id=item["espn_id"]
        except:
            espn_id=0
            
        try:
            height=item["height"]
        except:
            height=0
        
        try:
            weight=item["weight"]
        except:
            weight=0
        
        try:
            college=item["college"]
        except:
            college=''
            
        try:
            twitter=item["twitter_username"]
        except:
            twitter=''
            
        cur.execute('''INSERT OR IGNORE INTO players (player_id,name,position,team,draft_year,draft_round,draft_pick,nfl_id,espn_id,height,weight,college,twitter) 
                                            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)''', (player_id,name,position,team,draft_year,draft_round,draft_pick,nfl_id,espn_id,height,weight,college,twitter))
        
    conn.commit()
        
        

initialize_db()
import_players('https://www61.myfantasyleague.com/2017/export?TYPE=players&DETAILS=1&SINCE=&PLAYERS=&JSON=1')
conn.close()