import MySQLdb as sqldb
import connect_db as conn
from db_utils import db_util as util
import mfl_api as mfl


class Main(conn.Connect, mfl.export):

	def	__init__(self):
		
		week= util()
		self.year= week.get_current_week()[1]
		self.week= week.get_current_week()[2]
		self.week_id= week.get_current_week()[0]
		self.connect()
		
	def job_list(self):
		
		self.cur.execute(
						"SELECT jc.job_id, jd.job_name FROM job_calendar jc LEFT JOIN job_dim jd ON (jd.job_id = jc.job_id) WHERE jc.week= %s",(self.week, )
						)
		job_list= [i for i in self.cur.fetchall()]				
		
		return (job_list)
		
	def run_jobs(self):
				
				for job in self.job_list():
					
					if job[0] == 1:
						print ("{} - {}".format(job[0], job[1]))
						print ("END STEP")
					elif job[0] == 2:
						print ("{} - {}".format(job[0], job[1]))
						print ("END STEP")
					elif job[0] == 3:
						print ("{} - {}".format(job[0], job[1]))
						print ("END STEP")
					elif job[0] == 4:
						print ("{} - {}".format(job[0], job[1]))
						print ("END STEP")
					
test= Main()
test.run_jobs()

