
league_id= 69302 
#21676
#69302 dev
username= "cmwillis02"
password= "02guam04"
year= 2017

proto= "https://"
host= "www61.myfantasyleague.com/"
json= 0
req_type= "salaries"


import requests
import xml.etree.ElementTree as ET
import time
import datetime
import sys


class ImportApi:

    def __init__(self, year):
        opener = request.build_opener()
        mfl_url = 'http://football.myfantasyleague.com'
        self.opener = opener
        self.mfl_import_url = '{}/{}/import'.format(mfl_url, year)
        self.mfl_login_url = '{}/{}/login'.format(mfl_url, year)

    _logged_in = False

    def _import(self, params, json=True):
        if json:
            params['JSON'] = 1
        encoded_params = urllib.urlencode(params)
        url = '{}?{}'.format(self.mfl_import_url, encoded_params)
        resp = self.opener.open(url)
        return resp.read()

    # To login as commissioner, franchise_id = '0000'
    def login(self, league_id, franchise_id, password):
        params = urllib.urlencode({
            'L': league_id,
            'FRANCHISE_ID': franchise_id,
            'PASSWORD': password,
            'XML': 1}) # is 'XML' required?
        url = '{}?{}'.format(self.mfl_login_url, params)
        resp = urllib2.urlopen(url)
        user_id = ET.fromstring(resp.read()).attrib['session_id']
        self.opener.addheaders.append(('Cookie', 'USER_ID={}'.format(user_id)))
        self.league_id = league_id
        self.franchise_id = franchise_id	
        self._logged_in = True # may not be needed