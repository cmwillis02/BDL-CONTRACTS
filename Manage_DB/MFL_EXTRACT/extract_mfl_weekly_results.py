import sqlite3
import urllib2
import json

path='C:\Users\cwillis\Desktop\BDL v3.0\Data\Landing\ETL_MFL_RAW.sqlite'

conn = sqlite3.connect(path)
cur = conn.cursor()

def initialize_db():

    
    cur.execute('''DROP TABLE IF EXISTS weeklyresults''')
    cur.execute('''CREATE TABLE weeklyresults ( id INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT,
                                                ffid INTEGER,
                                                franchise_id INTEGER,
                                                year INTEGER,
                                                week INTEGER,
                                                matchup_id INTEGER,
                                                result TEXT,
                                                player_id INTEGER,
                                                score REAL,
                                                roster_status TEXT)''')

        


def create_mfl_json(server, year, week, league_id):
    
    url = 'http://www' + str(server) + '.myfantasyleague.com/' + str(year) + '/export?TYPE=weeklyResults&L=' + str(league_id) + '&W=' + str(week) + '&JSON=1'
    uh = urllib2.urlopen(url)
    data = uh.read()
    js=json.loads(str(data))
    print url
    
    return js


def parse_players(players, year, week, franchise_id, m_id, result):

    for player in players:
        player_id=player["id"]
        score=player["score"]
        status=player["status"]
        ffid=((year*100) + (week))*100 + int(franchise_id)
        print 'Year-Week',year, week,'Franchise',franchise_id, result

        cur.execute(
                        '''INSERT INTO weeklyresults (ffid, franchise_id, year, week, matchup_id, result, player_id, score, roster_status)
                                              VALUES (?,?,?,?,?,?,?,?,?) ''', (ffid, franchise_id, year, week,m_id, result, player_id, score, status) 
                            )
    
    
def import_weekly_results(server, year, week, league_id):
    
    js=create_mfl_json(server, year, week, league_id)
    
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
        	print item
            franchise_id=item["id"]
            try:
                result=item["result"]
            except:
                result= 'T'
            players=item["player"]
            
            parse_players(players, year, week, franchise_id, m_id, result)
                                        
    conn.commit()
    
def import_bye_weeks(server, year, week, league_id):
    
    js=create_mfl_json(server, year, week, league_id)
    
    for item in js["weeklyResults"]["franchise"]:
        franchise_id=item["id"]
        result='BYE'
        m_id=None
        
        players=item["player"]
        
        parse_players(players, year, week, franchise_id,m_id, result)
    
    conn.commit()
    

def run_process(server, year, league_id):
        
        for week in range(1,2):
            if week in [14,15,16]:
                import_weekly_results(server, year, week, league_id)
                import_bye_weeks(server, year, week, league_id)
            else:
                import_weekly_results(server, year, week, league_id)

            

initialize_db()
run_process(61, 2017, 21676)

conn.close()