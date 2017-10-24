import psycopg2
import sys

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


	
week_id= int(input("Enter week to reset: ", ))

if week_id == 99:

	run_yn= input("RESET ALL WEEKS? (y/n): ", )
	
	if run_yn == 'y':
		cur.execute(
					"UPDATE contracts_week SET run_status = 0"
					)
	
		cur.execute(
					"DELETE FROM contracts_player_fact"
					)
	
		cur.execute(
					"DELETE FROM contracts_franchise_fact"
					)

		conn.commit()
	
		print ('ALL WEEKS RESET')
	else:
		sys.exit(1)
else:
	cur.execute(
				"UPDATE contracts_week SET run_status = 0 WHERE week_id = %s", (week_id, )
				)
	
	cur.execute(
				"DELETE FROM contracts_player_fact WHERE week_id = %s", (week_id, )
				)
	
	cur.execute(
				"DELETE FROM contracts_franchise_fact WHERE week_id = %s", (week_id, )
				)

	conn.commit()

	