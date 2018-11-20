import json
import logging
import logging.config
from os import path, remove, rename

import MySQLdb as sqldb

import BDL_fact
import manage_db
import mfl_api
import player_dimension
import roster



def run_job(job_id):
    logger.info("BEGIN JOB:  {}".format(job_id))
    if job_id == 1:
        #Create MFL json
        logger.info("BEGIN EXTRACT:  PLAYER_DIM")
        json_data= mfl.player_dim()
        logger.info("END EXTRACT:  PLAYER_DIM")

        #Create player process object
        logger.info("BEGIN TRANSFORM:  PLAYER_DIM")
        player_load_obj = player_dimension.Player(json_data)
        player_load_list= player_load_obj.load_players()
        logger.info("END TRANSFORM:  PLAYER_DIM")

        #Load Player List
        logger.info("BEGIN LOAD:  PLAYER_DIM")
        DB.load_player_dim(player_load_list)
        logger.info("END LOAD:  PLAYER_DIM")

    if job_id == 2:
        logger.info("BEGIN EXTRACT:  ROSTER")
        json_data= mfl.rosters()
        logger.info("END EXTRACT:  ROSTER")

        logger.info("BEGIN TRANSFORM:  ROSTER")
        current_contracts= DB.current_contracts()
        roster_obj = roster.Roster(json_data, current_contracts)
        roster_obj.process_rosters()
        logger.info("END TRANSFORM:  ROSTER")

        logger.info("BEGIN LOAD:  ROSTER")
        DB.load_contracts(roster_obj.contract_updates)
        logger.info("END LOAD:  ROSTER")

    if job_id == 3:
        #Create MFL json
        logger.info("BEGIN EXTRACT:  FACT")
        player_scores_json= mfl.player_scores()
        weekly_results_json= mfl.weekly_results()

        logger.debug(json.dumps(player_scores_json, sort_keys= True, indent= 4))
        logger.info("EXTRACT:  WEEKLY RESULTS")
        logger.debug(json.dumps(weekly_results_json, sort_keys= True, indent= 4))
        logger.info("END EXTRACT:  FACT")

        #Create fact process Object
        logger.info("BEGIN TRANSFORM:  FACT")
        bdl_fact= BDL_fact.BDL_Fact(player_scores_json, weekly_results_json, DB.week_id)
        bdl_fact.main_process()

        logger.info("END TRANSFORM:  FACT")

        logger.info("BEGIN LOAD: FRANCHISE FACT")
        DB.load_franchise_fact(bdl_fact.matchups_to_load)
        logger.info("END LOAD: FRANCHISE FACT")

        logger.info("BEGIN LOAD:  PLAYER FACT")
        DB.load_player_fact(bdl_fact.players_to_load)
        logger.info("END LOAD:  PLAYER FACT")


    if job_id == 4:
        DB.set_playoffs()
    logger.info("END JOB:  {}".format(job_id))



if __name__ == "__main__":

##### Logging object configuration ####
    if path.isfile('logs/main_process.log'):
    	remove('logs/main_process.log')
    with open("config/logging_config.json", 'r') as logging_configuration_file:
    	config_dict = json.load(logging_configuration_file)
    logging.config.dictConfig(config_dict)
    logger = logging.getLogger(__name__)


    logger.info("----------")
    logger.info("BEGIN:  MAIN PROCESS")
    logger.info("----------")

    logger.info("SETUP DB CONNECTION")
    ##Create Database Management Object
    DB= manage_db.Manage_db()

    logger.info("Week_id= {}".format(DB.week_id))
    print ("Main Process Run for {}".format(DB.week_id))
    logger.info("MFL Server + League_ID:  {}".format(DB.get_mfl_connection()))
    logger.info("DB CONNECTED")

    logger.info("SETUP MFL CONNECTION")

    ##Create MFL Connection Object
    mfl= mfl_api.Export(DB.year, DB.week, DB.get_mfl_connection())
    mfl.login()

    logger.info("MFL CONNECTED")

    logger.info("BEGIN:  RUN JOBS")
    for i in DB.get_job_list():
        run_job(i[0])
    logger.info("END:  RUN JOBS")

    DB.close_week()

    rename("logs/main_process.log", "logs/main_process_{}.log".format(DB.week_id))

    logger.info("----------")
    logger.info("END:  MAIN PROCESS")
    logger.info("----------")
