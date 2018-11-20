from datetime import date
import logging
import sys

import MySQLdb as sqldb


class Manage_db(object):

    def __init__(self):

        self.logger= logging.getLogger(__name__)

        self.logger.info("Connecting to localhost DB= BDLCORE")
        self.db=sqldb.connect(
        				host="localhost",
        				user="root",
        				passwd="Bdladmin!23",
        				db="BDLCORE")
        self.cur= self.db.cursor()
        self.logger.info("Connected to BDLCORE")

        self.logger.info("Collecting current week")
        self.cur.execute("SELECT week_id, year, week FROM contracts_week WHERE run_status= 0 AND week_id= (SELECT min(week_id) FROM contracts_week WHERE run_status= 0)")
        results= self.cur.fetchall()[0]

        self.week_id= results[0]
        self.year= results[1]
        self.week= results[2]
        self.logger.info("Week_id= {}, year= {}, week= {}".format(self.week_id, self.year, self.week))

        self.playoff_list = [
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
							(201716,5,9),
							]

    def commit(self):

        self.db.commit()

    ### UTIL METHODS ###

    def get_mfl_connection(self):

        self.cur.execute(
        				"SELECT league_id, url FROM url_reference WHERE year = %s",(self.year,)
        				)
        results= self.cur.fetchall()[0]

        self.logger.info("Year= {}  ---  MFL Connection info= {}".format(self.year, results))

        return results

    def get_job_list(self):

        self.cur.execute(
        				"SELECT jc.job_id, jd.job_name FROM job_calendar jc LEFT JOIN job_dim jd ON (jd.job_id = jc.job_id) WHERE jc.week= %s AND jd.active_flg= 1",(self.week, )
        				)
        job_list= [i for i in self.cur.fetchall()]

        self.logger.info("Job List= {}".format(job_list))

        return (job_list)

    def close_week(self):

        self.logger.info("CLOSE WEEK {}".format(self.week_id))

        self.cur.execute(
        				"UPDATE contracts_week SET run_status = 1 WHERE week_id= %s",(self.week_id,)
        				)
        self.logger.info("Week= {} Run_status = 1".format(self.week_id))

        self.commit()

    def decrement_years(self):

        self.cur.execute(
        				"UPDATE contracts_contract SET years_remaining = years_remaining -1 WHERE current_ind = 1"
        				)
        self.commit("DECREMENT YEARS")

    def reset_week(self, week_id):

        self.cur.execute(
                        "DELETE FROM history_player_fact WHERE week_id >= %s",(week_id,)
        )
        self.cur.execute(
                        "DELETE FROM history_franchise_fact WHERE week_Id >= %s",(week_id,)
        )
        self.cur.execute(
                        "UPDATE contracts_week SET run_status = 0 WHERE week_id >= %s",(week_id,)
        )
        self.commit()

    def set_playoffs(self):

        ## TODO NEED TO UPDATE LOGIC TO ACCOUNT FOR POSTSEASON BYES + TOILET BOWL GAMES
        for row in self.playoff_list:
            self.logger.info("SET PLAYOFF MATCHUP:  {} - {} - {}".format(row[0], row[1], row[2]))
            self.cur.execute(
                        "UPDATE history_franchise_fact SET matchup_type = %s WHERE week_id = %s AND franchise_id = %s", ('p', row[0], row[1])
                        )

            self.cur.execute(
                        "UPDATE history_franchise_fact SET matchup_type = %s WHERE week_id = %s and franchise_id = %s", ('p', row[0], row[2])
                        )
        self.commit()

    def load_err(self):
        pass
        ## When loading records if an error is caught append that record to error dataset.

    def current_contracts(self):
        self.logger.info("PULL CURRENT CONTRACTS")

        self.cur.execute(
                            "SELECT player_id, franchise_id, id FROM contracts_contract WHERE current_ind = true"
                        )

        current_contracts= self.cur.fetchall()
        self.logger.debug(current_contracts)

        return current_contracts

    ###  LOAD DATA METHODS  ###
    def load_player_dim(self, player_list):

        list_count= 0
        loaded_count= 0
        reject_count= 0
        for i in player_list:
            list_count = list_count +1
            try:
                self.cur.execute(
                				"INSERT INTO contracts_player (player_id, position, name) VALUES (%s, %s, %s)",(i[0], i[2], i[1])
                				)
                self.logger.info("DB LOAD(PLAYER):  {} - {} - {}".format(i[0], i[2], i[1]))
                loaded_count = loaded_count + 1
                self.commit()

            except (sqldb.Error, sqldb.Warning) as e:
                self.db.rollback()
                self.logger.warning("DB REJECT(PLAYER):  {} --  {} - {} - {}".format(e, i[0], i[2], i[1]))
                reject_count = reject_count + 1

        self.logger.info("COMMIT PLAYERS:  Total= {}, Loaded= {}, Rejected= {}".format(list_count, loaded_count, reject_count))

    def load_franchise_fact(self, matchup_list):

        self.logger.info("DB LOAD(FRANCHISE_FACT)")

        list_count= 0
        load_count= 0
        error_count= 0

        for i in matchup_list:
            list_count= list_count + 1

            franchise_id= i[1]
            total_score= i[3]
            result= i[2]
            opponent_id= i[5]
            opponent_score= i[6]
            if self.week_id in [14,15,16]:
                matchup_type= 'n'
            else:
                matchup_type= 'r'

            self.logger.info("MATCHUP LOADED: {} - {} - {} - {} - {} - {}".format(self.week_id, franchise_id, total_score, result, opponent_id, opponent_score))

            try:
                self.cur.execute(
                                "INSERT INTO history_franchise_fact (week_id, franchise_id, total_score, result, opponent_id, opponent_score, matchup_type) VALUES (%s, %s, %s, %s, %s, %s, %s)",(self.week_id, franchise_id, total_score, result, opponent_id, opponent_score, matchup_type)
                )
                load_count= load_count + 1
                self.commit()

            except (sqldb.Error, sqldb.Warning) as e:
                self.db.rollback()
                self.logger.warning("DB REJECT(FRANCHISE_FACT):  {} --  {} - {}".format(e, self.week_id, i[1]))
                error_count = error_count + 1

        self.logger.info("COMMIT FRANCHISE_FACT: Total= {}, Loaded= {}, Rejected= {}".format(list_count, load_count, error_count))


    def load_player_fact(self, players_to_load):

        self.logger.info("DB LOAD(PLAYER_FACT)")

        list_count= 0
        load_count= 0
        error_count= 0

        for i in players_to_load:
            list_count= list_count + 1

            player_id= i[0]
            franchise_id= i[3]
            score= i[2]
            status= i[1]

            self.logger.info("PLAYER LOADED:  {} - {} - {} - {}".format(player_id, franchise_id, score, status))

            try:
                self.cur.execute(
                					"INSERT INTO history_player_fact (player_id, franchise_id, week_id, score, roster_status) VALUES (%s, %s, %s, %s, %s)",(player_id, franchise_id, self.week_id, score, status)
                					)
                load_count= load_count + 1
                self.commit()

            except (sqldb.Error, sqldb.Warning) as e:
                self.db.rollback()
                self.logger.warning("DB REJECT(PLAYER FACT):  {} --  {} - {}".format(e, self.week_id, i[0]))
                error_count = error_count + 1

        self.logger.info("COMMIT PLAYER FACT: Total= {}, Loaded= {}, Rejected= {}".format(list_count, load_count, error_count))


    ###  Contract Methods (Add Update Close) ###
    def load_contracts(self, contract_update_list):

        for contract in contract_update_list:
            if contract[0] == 'New':
                ## Add a new contract.
                self.cur.execute(
                                "INSERT INTO contracts_contract (player_id, franchise_id, current_ind, roster_status, date_assigned, years, years_remaining) VALUES (%s, %s, %s, %s, %s, %s, %s)",(contract[1]['player_id'], contract[1]['franchise_id'], 1, contract[1]['status'], date.today(),contract[1]['years'], contract[1]['years'])
                )
                self.commit()

                self.logger.info("LOAD CONTRACT:  {} - {}".format(contract[1]['player_id'], contract[1]['franchise_id']))

            elif contract[0] == 'Update':
                ## Add a new contract and close the previous contract.
                self.cur.execute(
                                "INSERT INTO contracts_contract (player_id, franchise_id, current_ind, roster_status, date_assigned, years, years_remaining) VALUES (%s, %s, %s, %s, %s, %s, %s)",(contract[1]['player_id'], contract[1]['franchise_id'], 1, contract[1]['status'], date.today(), contract[1]['years'], contract[1]['years'])
                )

                self.logger.info("LOAD CONTRACT:  {} - {}".format(contract[1]['player_id'], contract[1]['franchise_id']))

                self.cur.execute(
                                "UPDATE contracts_contract SET current_ind = 0, date_terminated= %s, years_remaining= %s, roster_status= %s WHERE id= %s",(today, None, None, contract[1]['previous_contract'])
                )
                self.logger.info("CLOSE PREVIOUS CONTRACT: {}".format(contract[1]['previous_contract']))
                self.commit()




## TEST DB CONNECTION##
if __name__ == "__main__":
    try:
        print ("{} - {} - {}".format(sys.argv[0], sys.argv[1], sys.argv[2]))
    except:
        print ("{} - {}".format(sys.argv[0], sys.argv[1]))

    if sys.argv[1] is "TEST":
        db= Manage_db()
        print ('TESTING Manage_db')
        print (db.week_id, db.year, db.week)
        print (db.get_mfl_connection())
        print (db.get_job_list())
        print ('TESTING Complete')

    if sys.argv[1] == "RESET":
        print ("RESET WEEK: {}".format(sys.argv[2]))

        db= Manage_db()
        db.reset_week(sys.argv[2])

    if sys.argv[1] == "PLAYOFFS":
        db= Manage_db()
        db.set_playoffs()
