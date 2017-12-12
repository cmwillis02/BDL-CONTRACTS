import psycopg2
import sys

# --- DATABASE CONNECTION --- #     

dsn_database= 'CORE'
dsn_hostname= 'bdlcompanion.cquxuyvkuxqs.us-east-1.rds.amazonaws.com'
dsn_port = '5432'
dsn_uid= 'bdladmin'
dsn_pwd= 'bdladmin!23'


try:
	conn_string= "host=" + dsn_hostname + " port=" + dsn_port+" dbname=" + dsn_database + " user=" + dsn_uid + " password=" + dsn_pwd
	conn= psycopg2.connect(conn_string)
	cur= conn.cursor()
	print ('Connected')
except:
	print ('Unable to connect')
	sys.exit(1)
	
playoff_list = [
					(200914,6,5),
					(200914,10,8),
					(200915,2,10),
					(200915,1,5),
					(200916,10,1),
					(201014,9,5),
					(201014,4,3),
					(201015,1,4),
					(201015,2,9),
					(201016,9,4),
					(201114,1,10),
					(201114,7,2),
					(201115,5,2),
					(201115,3,1),
					(201116,3,2),
					(201214,1,7),
					(201214,4,9),
					(201215,6,9),
					(201215,2,1),
					(201216,1,9),
					(201314,2,10),
					(201314,9,3),
					(201315,4,3),
					(201315,7,10),
					(201316,4,10),
					(201414,4,10),
					(201414,5,7),
					(201415,6,5),
					(201415,3,10),
					(201416,6,3),
					(201514,6,8),
					(201514,5,3),
					(201515,7,6),
					(201515,4,3),
					(201516,7,4),
					(201614,4,8),
					(201614,6,7),
					(201615,2,4),
					(201615,5,6),
					(201616,6,2),
					(201714,9,10),
					(201714,3,5),
					(201715,2,9),
					(201715,4,5),
					]

for row in playoff_list:
	
	cur.execute(
				"UPDATE contracts_franchise_fact SET matchup_type = %s WHERE week_id = %s AND franchise_id = %s", ('p', row[0], row[1])
				)
	
	cur.execute(
				"UPDATE contracts_franchise_fact SET matchup_type = %s WHERE week_id = %s and franchise_id = %s", ('p', row[0], row[2])
				)
	
conn.commit()