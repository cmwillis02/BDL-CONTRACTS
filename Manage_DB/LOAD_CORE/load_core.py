import psycopg2
import sqlite3

core_conn = psycopg2.connect(host="bdlpg.cquxuyvkuxqs.us-east-1.rds.amazonaws.com", port="5432", dbname='BDLCORE', user="bdladmin", password="bdladmin123")
core=core_conn.cursor()

stage_path= 'C:\Users\cwillis\Desktop\BDL v3.0\Data\Stage\BDL_STAGE.sqlite'
stage_conn = sqlite3.connect(stage_path)
stage = stage_conn.cursor()
  

   
def load_table(type):
    
    error_count=0
    
    query='PRAGMA table_info('+type+')'  
    stage.execute(query)
    columns = stage.fetchall()
    
    column_num= len(columns)
    
    query= 'SELECT * FROM ' + type
    stage.execute(query)
    results = stage.fetchall()
    results_num=len(results)
    
    for i in range(0,column_num):
        if i==0:
            fields=columns[i][1]
            values='%s'
            inserts='record["c' + str(i) + '"]'
        else:
            fields=fields + ',' + columns[i][1]
            values=values + ',' + '%s'
            inserts=inserts + ', record["c' + str(i) + '"]'
    
    insert_query="INSERT INTO " + type + " (" + fields + ") " + "VALUES ("+values+")"
    print insert_query
    
    for row in results:
        
        try:
            core.execute(insert_query, row)
            print row
            
        except psycopg2.IntegrityError:
            core_conn.rollback()
        
    

#load_table('week_dim')
#load_table('franchise_dim')
#load_table('player_dim')
#load_table('franchise_fact')
#load_table('player_fact')
#load_table('roster_current')
#load_table('standings_current')
#load_table('seasons_fact')

