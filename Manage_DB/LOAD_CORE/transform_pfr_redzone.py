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

#Used for updating null values while uploading existing records.
def null_test(i, row):
    
    value = row[i]
    if value is None or value == '':
        return 0
    else:
        return value
        

def append_rz():
    landing.execute(
                            ''' SELECT   p.*, ru.*, re.*    
                                            FROM rz_passing p
                                            LEFT JOIN rz_rushing ru on (ru.pid = p.pid and ru.year = p.year)
                                            LEFT JOIN rz_receiving re on (re.pid = p.pid and re.year = p.year)
                                            
                                            UNION
                                            
                                SELECT   p.*, ru.*, re.*   
                                            FROM rz_rushing ru
                                            LEFT JOIN rz_passing p on (p.pid = ru.pid and p.year = ru.year)
                                            LEFT JOIN rz_receiving re on (re.pid = ru.pid and re.year = ru.year)
                                            
                                            UNION
                                            
                                SELECT   p.*, ru.*, re.*   
                                            FROM rz_receiving re
                                            LEFT JOIN rz_passing p on (p.pid = re.pid AND p.year = re.year)
                                            LEFT JOIN rz_rushing ru on (ru.pid = re.pid AND ru.year = re.year)
                                        
                                        '''
                                      )
                                      
    results=landing.fetchall()

    for row in results:
        
        if row[2] is not None:
            pfr_id=row[2]
        elif row[20] is not None:
            pfr_id= row[20]
        else:
            pfr_id= row[38]
        
        if row[3] is not None:
            year= row[3]
        elif row[21] is not None:
            year= row[21]
        else:
            year= row[39]
        
        if row[1] is not None: 
            name= row[1]
        elif row[20] is not None:
            name= row[20]
        else:
            name=row[38]
        
        core.execute(
                        '''SELECT player_id FROM player_dim WHERE pfr_id = %s''',(pfr_id,)
                        )
        
        try:
            player_id=core.fetchall()[0][0]
        
        except:
            error.execute(
                            ''' INSERT INTO pfr_id (pfr_id, year, name) VALUES (?, ?, ?)''',(pfr_id, year, name)
                            )
            print pfr_id, year, name, 'NO MATCH'
            continue

        rz_ps_att= null_test(5, row)
        rz_ps_cmp= null_test(7, row)
        rz_ps_yds= null_test(15, row)
        rz_ps_td= null_test(13, row)
        rz_ps_int= null_test(11, row)
        
        rz_ps_10_att= null_test(6, row)
        rz_ps_10_cmp= null_test(8, row)
        rz_ps_10_yds= null_test(16, row)
        rz_ps_10_td= null_test(14, row)
        rz_ps_10_int= null_test(12, row)
        
        rz_ru_att= null_test(23, row)
        rz_ru_yds= null_test(32, row)
        rz_ru_td= null_test(29, row)
        
        rz_ru_10_att= null_test(24, row)
        rz_ru_10_yds= null_test(33, row)
        rz_ru_10_td= null_test(30, row)
        
        rz_ru_5_att= null_test(26, row)
        rz_ru_5_yds= null_test(34, row)
        rz_ru_5_td= null_test(31, row)
        
        rz_re_tgt= null_test(49, row)
        rz_re_rec= null_test(43, row)
        rz_re_yds= null_test(47, row)
        rz_re_td= null_test(45, row)
        
        rz_re_10_tgt= null_test(50, row)
        rz_re_10_rec= null_test(44, row)
        rz_re_10_yds= null_test(48, row)
        rz_re_10_td=  null_test(46, row)
        
        stage.execute(
                        '''UPDATE seasons_fact  SET rz_ps_att= ?, 
                                                    rz_ps_cmp= ?,
                                                    rz_ps_yds= ?,
                                                    rz_ps_td= ?, 
                                                    rz_ps_int= ?,
                                                    rz_ps_10_att= ?,
                                                    rz_ps_10_cmp= ?, 
                                                    rz_ps_10_yds= ?,
                                                    rz_ps_10_td= ?,
                                                    rz_ps_10_int= ?,
                                                    rz_ru_att= ?,
                                                    rz_ru_yds= ?,
                                                    rz_ru_td= ?,
                                                    rz_ru_10_att= ?,
                                                    rz_ru_10_yds= ?, 
                                                    rz_ru_10_td= ?,
                                                    rz_ru_5_att= ?,
                                                    rz_ru_5_yds= ?,
                                                    rz_ru_5_td= ?,
                                                    rz_re_tgt= ?,
                                                    rz_re_rec= ?,
                                                    rz_re_yds= ?,
                                                    rz_re_td= ?,
                                                    rz_re_10_tgt= ?,                                                
                                                    rz_re_10_rec= ?,
                                                    rz_re_10_yds= ?,
                                                    rz_re_10_td= ?
                                                    
                                                    WHERE player_id = ? AND year = ?
                                                    ''',
                                                    
                                                    ( rz_ps_att , rz_ps_cmp , rz_ps_yds , rz_ps_td , rz_ps_int , rz_ps_10_att , rz_ps_10_cmp , 
                                                    rz_ps_10_yds , rz_ps_10_td , rz_ps_10_int , rz_ru_att , rz_ru_yds , rz_ru_td , rz_ru_10_att , rz_ru_10_yds , 
                                                    rz_ru_10_td , rz_ru_5_att , rz_ru_5_yds , rz_ru_5_td , rz_re_tgt , rz_re_rec , rz_re_yds , rz_re_td , rz_re_10_tgt , 
                                                    rz_re_10_rec , rz_re_10_yds , rz_re_10_td, player_id, year)
                            )
        
        print player_id, year, 'MATCHED'

    stage_conn.commit()
    error_conn.commit()

    #Used to update null values that exist b/c there was no record of that type for that player (eg. Receiving stats for a QB)
def update_nulls():
    stage.execute(
                    '''SELECT player_id FROM seasons_fact WHERE rz_ps_att IS NULL'''
                    )

    results= stage.fetchall()

    for row in results:
        player_id= row[0]
        
        stage.execute(''' UPDATE seasons_fact SET   rz_ps_att= ?, 
                                                    rz_ps_cmp= ?,
                                                    rz_ps_yds= ?,
                                                    rz_ps_td= ?, 
                                                    rz_ps_int= ?,
                                                    rz_ps_10_att= ?,
                                                    rz_ps_10_cmp= ?, 
                                                    rz_ps_10_yds= ?,
                                                    rz_ps_10_td= ?,
                                                    rz_ps_10_int= ?,
                                                    rz_ru_att= ?,
                                                    rz_ru_yds= ?,
                                                    rz_ru_td= ?,
                                                    rz_ru_10_att= ?,
                                                    rz_ru_10_yds= ?, 
                                                    rz_ru_10_td= ?,
                                                    rz_ru_5_att= ?,
                                                    rz_ru_5_yds= ?,
                                                    rz_ru_5_td= ?,
                                                    rz_re_tgt= ?,
                                                    rz_re_rec= ?,
                                                    rz_re_yds= ?,
                                                    rz_re_td= ?,
                                                    rz_re_10_tgt= ?,                                                
                                                    rz_re_10_rec= ?,
                                                    rz_re_10_yds= ?,
                                                    rz_re_10_td= ?
                                                    
                                                    WHERE player_id = ?''',
                                                    (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, player_id)
                            )
        print player_id, 'Updating Null Values'
        stage_conn.commit()

append_rz()        
update_nulls()