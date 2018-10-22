#!/usr/bin/python3.6

import json
import logging

import MySQLdb as mysql



class BDL_Fact():

    def __init__(self, player_scores_json, weekly_results_json, week_id):

        ##Create logging object ##
        self.logger= logging.getLogger(__name__)

        self.player_scores_json= player_scores_json
        self.weekly_results_json= weekly_results_json
        self.players_to_load= []
        self.teams_to_load= []
        self.matchups_to_load= []
        self.week_id= week_id


    def main_process(self):

        self.logger.info("BEGIN:  FACT MAIN PROCESS")
        self.weekly_results()
        self.player_scores()
        self.set_matchups()

        self.logger.info("END:  FACT MAIN PROCESS")

    def player_scores(self):

        self.logger.info("BEGIN PROCESS:  FACT PLAYER SCORES")
        for item in self.player_scores_json["playerScores"]["playerScore"]:
            load_player= 1
            status='f'
            score = float(item["score"])
            player_id = item["id"]
            franchise_id= None

            for player in self.players_to_load:
                if player[0] == player_id:
                    load_player=0
                    break
                else:
                    continue

            if load_player == 1:
                self.players_to_load.append((player_id, status, score, franchise_id))

        self.logger.info("players_to_load - {}".format(self.players_to_load))
        self.logger.info("END PROCESS: FACT PLAYER SCORES")


    def weekly_results(self):
		#Some weeks require fewer than 5 matchup ids, work up from 0 and except: once finished

        matchups= 0
        for matchup_id in range(0,5):
            self.logger.info("matchup_id = {}".format(matchup_id))
            try:
                matchup= self.weekly_results_json["weeklyResults"]["matchup"][matchup_id]["franchise"]
                matchups= matchup_id
            except:
                self.logger.warning("MATCHUP ID NOT FOUND")
                break

        for matchup_id in range(0,matchups+1):

            self.logger.debug("JSON RAW MATCHUP= {}  {}".format(matchup_id, json.dumps(self.weekly_results_json["weeklyResults"]["matchup"][matchup_id], indent= 4)))
            for item in self.weekly_results_json["weeklyResults"]["matchup"][matchup_id]["franchise"]:
                franchise_id= item["id"]

                self.logger.info("MATCHUP:  {}  --  FRANCHISE:  {}".format(matchup_id, franchise_id))

                total_score= 0
                players= item["player"]

                try:
                    result= item["result"].lower()
                except:
                    result= 't'

                for player in players:

                    self.logger.debug("JSON RAW PLAYERS - {}".format(json.dumps(player, sort_keys= True, indent= 4)))
                    player_id= player["id"]

                    try:
                        score= player["score"]
                        if player["score"] == '':
                            score= 0
                        else:
                            score= player["score"]
                    except:
                        score= 0

                    if player["status"] == 'starter':
                        status= 's'
                        total_score= float(total_score) + float(score)
                    else:
                        status= 'b'

                    self.logger.info("APPEND PLAYER:  {} - {} - {} - {}".format(player_id, status, score, franchise_id))
                    self.players_to_load.append((player_id, status, score, franchise_id))

                self.logger.info("APPEND FRANCHISE:  {} - {} - {} - {}".format(matchup_id, franchise_id, result, total_score))
                self.teams_to_load.append((matchup_id, franchise_id, result, total_score))

        ## Load bye week franchises
        for item in self.weekly_results_json["weeklyResults"]["franchise"]:
            franchise_id= item["id"]
            matchup_id = None

            self.logger.info("MATCHUP:  {}  --  FRANCHISE:  {}".format(matchup_id, franchise_id))

            total_score= 0
            players= item["player"]
            result = 'b'

            for player in players:

                self.logger.debug("JSON RAW PLAYERS - {}".format(json.dumps(player, sort_keys= True, indent= 4)))
                player_id= player["id"]

                try:
                    score= player["score"]
                    if player["score"] == '':
                        score= 0
                    else:
                        score= player["score"]
                except:
                    score= 0

                if player["status"] == 'starter':
                    status= 's'
                    total_score= float(total_score) + float(score)
                else:
                    status= 'b'

                self.logger.info("APPEND PLAYER:  {} - {} - {} - {}".format(player_id, status, score, franchise_id))
                self.players_to_load.append((player_id, status, score, franchise_id))

            self.logger.info("APPEND FRANCHISE:  {} - {} - {} - {}".format(matchup_id, franchise_id, result, total_score))
            self.teams_to_load.append((matchup_id, franchise_id, result, total_score))

        self.logger.info("RESULTS LIST")
        self.logger.info(self.players_to_load)
        self.logger.info("MATCHUP LIST")
        self.logger.info(self.teams_to_load)

    def set_matchups(self):

        self.logger.info("BEGIN PROCESS: SET MATCHUPS")
        for team in self.teams_to_load:
            m_id= team[0]
            franchise_id= team[1]
            result= team[2]
            total_score= team[3]
            matchup_type = 'r'

            if m_id != None:
                for team2 in self.teams_to_load:
                    if team2[0] == m_id and team2[1] != franchise_id:
                        opponent_id= team2[1]
                        opponent_score= team2[3]
                    else:
                        continue
            elif m_id == None:
                opponent_id= None
                opponent_score= None

            self.logger.info("MATCHUP LOADED:  {} - {} - {} - {} - {} - {}".format(franchise_id, result, total_score, matchup_type, opponent_id, opponent_score))
            self.matchups_to_load.append((m_id, franchise_id, result, total_score, matchup_type, opponent_id, opponent_score))

        self.logger.info("matchups_to_load:  {}".format(self.matchups_to_load))

        self.logger.info("END PROCESS: SET MATCHUPS")

if __name__ == "__main__":
	api= mfl.export()

	#Create Fact class
	process= Fact(api.player_scores(), api.weekly_results, util.get_current_week()[0])
	process.main_process()
