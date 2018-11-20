import datetime
import json
import logging
import sys
import time


class Roster():

    def __init__(self, roster_json, current_contracts):

        self.roster_json= roster_json
        self.contract_updates= []
        self.current_contracts= current_contracts

        self.logger= logging.getLogger(__name__)

    def process_rosters(self):

        for franchise in range(0,10):

            franchise_id= franchise + 1
            for item in self.roster_json["rosters"]["franchise"][franchise]["player"]:
                player_id= item['id']
                if item['status'] == 'INJURED_RESERVE':
                    status == 'i'
                else:
                    status= 'r'
                years= max(int(item['contractYear']), 0)
                self.logger.info("CONTRACT:  {} - {} - {} - {}".format(franchise_id, player_id, years, status))

                contract_action= "New"
                for current in self.current_contracts:
                    if current[0] == player_id:
                        if current[1] == franchise_id:
                            contract_action= "Pass"
                            break
                        else:
                            contract_action= "Update"
                            previous_contract= current[2]
                            break

                if contract_action == 'New':
                    self.contract_updates.append(("New", {'player_id' : player_id, 'franchise_id' : franchise_id, 'status' : status, 'years' : years}))
                if contract_action == 'Update':
                    self.contract_updates.append(("Update", {'player_id' : player_id, 'franchise_id' : franchise_id, 'status' : status, 'years' : years,  'previous_contract' : previous_contract}))

        self.logger.info("CONTRACT UPDATES:  {}".format(self.contract_updates))
