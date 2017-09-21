import sqlite3

stage_path= 'C:\Users\cwillis\Desktop\BDL v3.0\Data\Stage\BDL_STAGE.sqlite'
landing_path= 'C:\Users\cwillis\Desktop\BDL v3.0\Data\Landing\ETL_MFL_RAW.sqlite'

stage_conn = sqlite3.connect(stage_path)
stage = stage_conn.cursor()

input_conn = sqlite3.connect(landing_path)
landing = input_conn.cursor()

def rosters():
    stage.execute('''DELETE FROM roster_current''')
    
    landing.execute(
                        ''' SELECT * FROM rosters '''
                        )
    results=landing.fetchall()
    
    for row in results:
        player_id = row[0]
        franchise_id = row[1]
        status= row[2]
        contract=row [3]
        
        print player_id, franchise_id, status, contract, 'ROSTER'
        
        stage.execute(
                        '''INSERT INTO roster_current (player_id, franchise_id, status, contract) VALUES (?, ?, ?, ?)''',(player_id, franchise_id, status, contract)
                        )
                        
    stage_conn.commit()

def standings():
    stage.execute('''DELETE FROM standings_current''')
       
    landing.execute(
                        ''' SELECT * FROM leaguestandings'''
                        )
    results=landing.fetchall()
    
    for row in results:
        franchise_id = row[0]
        wins= row[1]
        losses= row[2]
        ties=row [3]
        bones=row[4]
        
        print franchise_id, wins, losses, 'STANDINGS'
        
        stage.execute(
                        '''INSERT INTO standings_current (franchise_id, wins, losses, ties, bones) VALUES (?, ?, ?, ?, ?)''',(franchise_id, wins, losses, ties, bones)
                        )
                        
    stage_conn.commit()    
    

rosters()
standings()