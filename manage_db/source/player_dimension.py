import logging

import MySQLdb as sqldb

class Player():

    def __init__(self, json_data):

        self.json_data= json_data
        self.position_dict= {
        		'QB':'q',
        		'RB':'r',
        		'WR':'w',
        		'TE':'t',
        		'PK':'k',
        		'Def':'d'
        		}

        #Create Logging object
        self.logger= logging.getLogger(__name__)

    def load_players(self):

        players_to_load= []
        timestamp= self.json_data["players"]["timestamp"]
        for player in self.json_data["players"]["player"]:

            self.logger.debug("PLAYER: {}".format(player))
            position= player["position"]

            if position not in ['QB','RB','WR','TE','PK','Def']:
                self.logger.debug("NOT LOADED: {} - {} Position not used in BDL".format(player["position"], player["id"]))
                continue

            position_code= self.position_dict[position]
            player_id= player["id"]
            name= player["name"]

            self.logger.debug("LOADED:  {}".format(player["id"]))
            players_to_load.append((player_id, name, position_code))

        self.logger.debug("PLAYERS TO LOAD:  {}".format(players_to_load))
        return players_to_load


if __name__ == "__main__":

	from util import mfl_api as mfl

	api= mfl.export()

	main_player_dim= Main_player_dim(api.player_dim())
	main_player_dim.load_players()
