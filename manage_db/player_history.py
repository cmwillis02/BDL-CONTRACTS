import psycopg2

class milestones(object):
	
	def __init__(self, week_id):
		
		self.dsn_database= 'CORE'
		self.dsn_hostname= 'bdlcompanion.cquxuyvkuxqs.us-east-1.rds.amazonaws.com'
		self.dsn_port = '5432'
		self.dsn_uid= 'bdladmin'
		self.dsn_pwd= 'bdladmin!23'
		self.week_Id= week_id
		
		try:
			conn_string= "host={} port={} dbname={} user={} password= {}".format(self.dsn_hostname, self.dsn_port, self.dsn_database, self.dsn_uid, self.dsn_pwd)
			self.conn=psycopg2.connect(conn_string)

			self.cur= self.conn.cursor()
		
		except:
			print ('Unable to Connect')
			sys.exit(1)
			
	def scoring(self):
	
		self.cur.execute(
						"SELECT player_id, sum(score) FROM history_player_fact WHERE week_id <= %s GROUP BY player_id HAVING sum(score) >= 500"
						)
		results= self.cur.fetchall()
		
		print (results)