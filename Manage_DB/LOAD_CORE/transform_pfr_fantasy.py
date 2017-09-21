import sqlite3
import psycopg2


stage_path= 'C:\Users\cwillis\Desktop\BDL v3.0\Data\Stage\BDL_STAGE.sqlite'
landing_path= 'C:\Users\cwillis\Desktop\BDL v3.0\Data\Landing\ETL_MFL_RAW.sqlite'
error_path= 'C:\Users\cwillis\Desktop\BDL v3.0\Data\Stage\Error_handle.sqlite'

core_conn = psycopg2.connect(host="bdlpg.cquxuyvkuxqs.us-east-1.rds.amazonaws.com", port="5432", dbname='BDLCORE', user="bdladmin", password="bdladmin123")
core=core_conn.cursor()


stage_conn = sqlite3.connect(stage_path)
stage = stage_conn.cursor()

landing_conn = sqlite3.connect(landing_path)
landing = landing_conn.cursor()

error_conn = sqlite3.connect(error_path)
error = error_conn.cursor()


landing.execute(
                        '''SELECT pid, player_link, year, age, fantasy_points, fantasy_pos,
                                  fantasy_rank_overall, fantasy_rank_pos,g, gs, pass_att, pass_cmp,
                                  pass_int, pass_td, pass_yds, player, rec, rec_td, rec_yds, rush_att,
                                  rush_yds, rush_td, targets, team FROM fantasy'''
                                  )
results=landing.fetchall()

error.execute('''DELETE FROM pfr_id''')

error_conn.commit()
stage_conn.commit()

for row in results:
    
    pfr_id = row[0]
    core.execute(
                    '''SELECT player_id FROM player_dim WHERE pfr_id = %s''',(pfr_id,)
                    )
    
    result=core.fetchone()
    
    
    if result is None:
        pfr_id = row[0]
        year = int(row[2])
        name = row[15]
        table= 'fantasy'
        
        print pfr_id, year, name, 'NO MATCH'
        error.execute(
                        '''INSERT INTO pfr_id (pfr_id, year, name) VALUES (?, ?, ?)''', (pfr_id, year, name)
                        )
        
    
    else:
        player_id=result[0]
        fields={}
        for i in range(0,24):
            if row[i] == '':
                fields['h'+str(i)]= 0
            else:
                fields['h'+str(i)]= row[i]
        stage.execute(
                       ''' INSERT INTO seasons_fact (player_id, team, year, age, games_played, games_started, ps_att, ps_cmp, ps_yds, ps_td, ps_int, 
                                                      ru_att, ru_yds, ru_td, re_tgt, re_rec, re_yds, re_td)
                                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                                                     (player_id, fields['h23'], fields['h2'], fields['h3'], fields['h8'], fields['h9'], fields['h10'], fields['h11'], fields['h14'], fields['h13'], fields['h12'],
                                                     fields['h19'], fields['h20'], fields['h21'], fields['h22'], fields['h16'], fields['h18'], fields['h17'])
                                                     )
        print player_id, 'MATCH'

stage_conn.commit()
error_conn.commit()
        
                                  

