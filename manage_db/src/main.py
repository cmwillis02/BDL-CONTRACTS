import MySQLdb as sqldb
from util import connect_db as conn
from util import db_utils as util
from util import mfl_api as mfl
from  main_player_dim import Main_player_dim as player
import main_rosters as roster
import main_fact as fact
import main_playoffs as playoffs

		
def run_job(job_id, job_name, week_id):
				
	if job_id == 1:
		print ("{} - {}".format(job_id, job_name))
		
		api= mfl.export()
		
		main_player_dim= player(api.player_dim())
		main_player_dim.load_players()
		
		print ("END {}".format(job_name))
		
	elif job[0] == 2:
		print ("{} - {}".format(job_id, job_name))
		
		api= mfl.export()
		process= roster.Main_roster(api.rosters())
		process.main_process()
		
		print ("END {}".format(job_name))
		
	elif job[0] == 3:
		print ("{} - {}".format(job_id, job_name))
		api= mfl.export()
		
		#Create Fact class
		process= fact.Fact(api.player_scores(), api.weekly_results, util.get_current_week()[0])
		process.main_process()
		
		print ("END STEP")
		
	elif job[0] == 4:
		print ("{} - {}".format(job_id, job_name))
		
		obj= playoffs.main_playoffs()
		obj.update()
		
		print ("END STEP")

		
		
	
					
if __name__ == "__main__":
# Collect current week and job schedule data
	util= util.db_util()
	week_data= util.get_current_week()

	week_id= week_data[0]
	year= week_data[1]
	week= week_data[2]

	job_list= util.get_job_list(week)

	print ("Running Jobs: {} for {} - W{}".format(job_list, year, week))

	for job in job_list:
		run_job(job[0], job[1], week_id)
	
	util.close_week()