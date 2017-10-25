import psycopg2
import sys
import datetime

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

cur.execute(
			"SELECT max(run_date) FROM job_log"
			)
datestamp= cur.fetchone()[0]
	
print(
    datetime.datetime.fromtimestamp(
        int(datestamp)
    ).strftime('%Y-%m-%d %H:%M:%S')
)