import json
import logging
import logging.config
from os import path, remove

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
		logger.info("STEP BEGIN: {} - {}".format(job_id, job_name))

		api= mfl.export()

		main_player_dim= player(api.player_dim())
		main_player_dim.load_players()

		logger.info("STEP END: {}".format(job_name))

	elif job[0] == 2:
		logger.info("STEP BEGIN: {} - {}".format(job_id, job_name))

		api= mfl.export()
		process= roster.Main_roster(api.rosters())
		process.main_process()

		logger.info("STEP END: {}".format(job_name))

	elif job[0] == 3:
		logger.info("STEP BEGIN: {} - {}".format(job_id, job_name))
		api= mfl.export()

		#Create Fact class
		process= fact.Fact(api.player_scores(), api.weekly_results, util.get_current_week()[0])
		process.main_process()

		logger.info("STEP END: {}".format(job_name))

	elif job[0] == 4:
		logger.info("STEP BEGIN: {} - {}".format(job_id, job_name))

		obj= playoffs.main_playoffs()
		obj.update()

		logger.info("STEP END: {}".format(job_name))





if __name__ == "__main__":

##### Logging object configuration ####
	if path.isfile('main_process.log'):
		remove('main_process.log')

	with open("logging_config.json", 'r') as logging_configuration_file:
		config_dict = json.load(logging_configuration_file)

	logging.config.dictConfig(config_dict)

	logger = logging.getLogger(__name__)

	logger.info('-------')
	logger.info('STEP BEGIN: main process')
	logger.info('-------')


#### Begin Main Process Code ####
	# Collect current week and job schedule data

	logger.info('STEP BEGIN: Job Setup')
	util= util.db_util()
	week_data= util.get_current_week()

	week_id= week_data[0]
	year= week_data[1]
	week= week_data[2]

	logger.info("WEEK ID: {}".format(week_id))
	logger.debug("year= {}".format(year))
	logger.debug("week= {}".format(week))


	job_list= util.get_job_list(week)
	logger.info("Job_list:  {}".format(job_list))

	logger.info('STEP END: Job Setup')

	logger.info('STEP BEGIN: Run Jobs')
	# for job in job_list:
	# 	run_job(job[0], job[1], week_id)

	logger.info('STEP END: Run Jobs')

	logger.info('STEP BEGIN: Close Week')
	util.close_week()
	logger.info('STEP END: Close Week')

	logger.info('-------')
	logger.info('End: main process')
	logger.info('-------')
