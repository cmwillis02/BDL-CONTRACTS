import sqlite3
import psycopg2

core_conn = psycopg2.connect(host="bdlpg.cquxuyvkuxqs.us-east-1.rds.amazonaws.com", port="5432", dbname='BDLCORE', user="bdladmin", password="bdladmin123")
core=core_conn.cursor()

landing_path= 'C:\Users\cwillis\Desktop\BDL v3.0\Data\Landing\ETL_MFL_RAW.sqlite'

input_conn = sqlite3.connect(landing_path)
landing = input_conn.cursor()

def load_player_dim():
    
    landing.execute(
                        '''SELECT * FROM players WHERE position in ('Def','WR','RB','QB','TE','PK') '''
                        )
                        
    records=landing.fetchall()
    
    for row in records:
        
        if row[2] in ['QB','RB','WR','TE','PK','Def']:
            
            player_id=row[0]
            name=row[1]
            position=row[2]
            team=row[3]
            draft_year=row[4]
            draft_round=row[5]
            draft_pick=row[6]
            nfl_id=row[7]
            espn_id=row[8]
            height=row[9]
            weight=row[10]
            college=row[11]
            twitter=row[12]
            
            try:
                core.execute(
                                '''INSERT OR IGNORE INTO player_dim (player_id, name, position, team, draft_year, draft_round, draft_pick, nfl_id, espn_id, height, weight, college, twitter)
                                                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)''',(player_id, name, position, team, draft_year, draft_round, draft_pick, nfl_id, espn_id, height, weight, college, twitter)
                                )
            except psycopg2.IntegrityError:
                core_conn.rollback()
            
        else:
            player_id=row[0]
            position=row[2]
            name=row[1]
    
    stage_conn.commit()
        
    
def load_player_fact():

    landing.execute(
                        '''SELECT player_id, year, week, "" AS franchise_id, score, "" as roster_status FROM playerscores'''
                            )
    results=landing.fetchall()
    records_read=len(results)
    records_loaded=0
    for row in results:
        player_id = row[0]
        year=row[1]
        week=row[2]
        score=row[4]
        actual_status = 'Active'
        
        
        landing.execute(
                            '''SELECT franchise_ID, roster_status FROM weeklyresults WHERE player_id = ? AND year= ? AND week=?''',(player_id, year, week)
                    )
        results=landing.fetchall()
        if len(results) == 0:
            franchise_id= None
            roster_status= None
        else:
            franchise_id=results[0][0]
            roster_status=results[0][1]
            
        core.execute(
                        '''SELECT week_id FROM week_dim WHERE year= ? and week= ?''',(year, week)
                        )
        week_id = stage.fetchall()[0][0]
        
        core.execute(
                        '''INSERT INTO player_fact (player_id, week_id, franchise_id, score, roster_status, actual_status)
                                             VALUES(?, ?, ?, ?, ?, ?)''',(player_id, week_id, franchise_id, score, roster_status, actual_status)
                        )
        records_loaded=+1
        
    stage_conn.commit()

def add_dnp_weeks():
    
    landing.execute(
                        '''SELECT player_id, year, week, score, roster_status, franchise_id FROM weeklyresults'''
                        )
                        
    results = landing.fetchall()
    
    for row in results:
        
        player_id=row[0]
        year=row[1]
        week=row[2]
        score=row[3]
        roster_status=row[4]
        franchise_id=row[5]
        actual_status = 'DNP'
        
        core.execute(
                        '''SELECT week_id FROM week_dim WHERE year= ? and week= ?''',(year, week)
                        )
        week_id = stage.fetchall()[0][0]
        
        core.execute(
                        '''SELECT player_id FROM player_fact WHERE week_id = ? AND player_id = ?''', (week_id, player_id)
                        )
                                        
        record=stage.fetchall()
        
        if len(record) != 0 :
            continue
            
        else:
            print player_id, week_id, score, roster_status, actual_status, franchise_id
            core.execute(
                            '''INSERT INTO player_fact (player_id, week_id, franchise_id, score, roster_status, actual_status)
                                                 VALUES(?, ?, ?, ?, ?, ?)''', (player_id, week_id, franchise_id, score, roster_status, actual_status)
                            )    
            
    stage_conn.commit()
    
    
# Type Parameter, truncate or reset
reset_db()
load_player_dim()
load_player_fact()
add_dnp_weeks()

stage.execute('''UPDATE player_fact SET score = 0.0 WHERE score=""''')
stage_conn.commit()




  

   
