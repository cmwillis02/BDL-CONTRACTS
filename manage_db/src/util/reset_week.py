import sys
import connect_db as conn

class manage_weeks(conn.Connect):
	
	def __init__(self):
		
		self.connect()
	
	def check_week(self, week):
		
		try:
			self.cur.execute(
							"SELECT run_status FROM contracts_week WHERE week_id = %s", (week, )
							)
			if self.cur.fetchall()[0][0] == 1:
				return week
			else:
				print ("{} has not been run".format(week))
				sys.exit(0)
				
		except:
			print ('No weeks reset')
			sys.exit(0)
	
	def reset_week(self, week_id):
	
		self.cur.execute(
				"UPDATE contracts_week SET run_status = 0 WHERE week_id = %s", (week_id, )
				)

		self.cur.execute(
					"DELETE FROM history_player_fact WHERE week_id = %s", (week_id, )
					)

		self.cur.execute(
					"DELETE FROM history_franchise_fact WHERE week_id = %s", (week_id, )
					)
		
		print ('{} has been reset run_status= 0'.format(week_id))
		self.commit()
		
if __name__ == "__main__":
	week= input('Reset Week:')
	
	obj= manage_weeks()
	obj.reset_week(obj.check_week(int(week)))
	

		
	