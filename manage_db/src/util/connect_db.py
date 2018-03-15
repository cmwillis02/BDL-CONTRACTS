import MySQLdb as sqldb


class Connect(object):
	
	def connect(self):
		
		self.db=sqldb.connect(
						host="localhost",
						user="root",
						passwd="Bdladmin!23",
						db="BDLCORE")
		self.cur= self.db.cursor()
		
	def commit(self, message=None):
		
		self.db.commit()
		if message:
			print ("Commit - {}".format(message))
		else:
			print ("Commit to Dev")
		
	def view_tables(self):
		"View all tables in DB connection"
		
		self.cur.execute("SHOW TABLES")
		
		print (self.cur.fetchall())
		
