
import requests
from bs4 import BeautifulSoup
import lxml
#import pymongo
from db_manager import DBManager
from pyevsim.system_simulator import SystemSimulator
from pyevsim.behavior_model_executor import BehaviorModelExecutor
from pyevsim.definition import *

#from pyevsim.system_executor import SysExecutor

#from env import Env

def fetch_weather_info(self):
    res = requests.get(self.w_url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")     

    sum = soup.find("dl", attrs={"class":"summary_list"})
    sensible_temp = sum.find_all("dd")[0].get_text() # 체감온도
    humidity = sum.find_all("dd")[1].get_text() # 습도
    wind = sum.find_all("dd")[2].get_text()
    temps_ = soup.find('div','temperature_text')
    temp=temps_.text.strip()[5:-1]


    edata = {
        'datetime' : datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'wbgt' : float(sensible_temp[:-1]),
        'temp' : float(temp),
        'humid' : float(humidity[:-1]),
        'wind' : float(wind[:-3])
        }

    return edata

import datetime
# envsim model class -> template 
class EnvSimModel(BehaviorModelExecutor):
    def __init__(self, inst_t, dest_t, mname, ename, config,fun):
        super().__init__(inst_t, dest_t, mname, ename)

        #self.db_url = f"mongodb://{config['env']['db_user']}:{config['env']['db_pw']}@{config['env']['db_addr']}"
        #self.db = pymongo.MongoClient(self.db_url)[config['env']['db_name']]

        self.db = DBManager(config, config['LOCAL']).get_database(config['env']['db_name'])
        
        self.w_url = config["env"]["naver_url"]
        self.config = config
        self.fun =fun


        # X
        self.insert_input_port("env_request")

        # Y
        self.insert_output_port("env")

        # State
        self.init_state("MONITOR")
        self.insert_state("MONITOR", 1)

        self.engine = SystemSimulator.get_engine(ename)

        if self.db[f"{self.config['env']['db_collection_name']}"].count_documents({}) == 0:
            self.env_info = self.fun()
            self.env_info_id = self.db[f"{self.config['env']['db_collection_name']}"].insert_one(self.env_info)
        else:
            cursors = self.db[f"{self.config['env']['db_collection_name']}"].find()
            self.env_info_id = cursors[0]["_id"]

    def ext_trans(self,port, msg):
        pass
    
    def output(self):
        
        self.env_info = self.fetch_weather_info()
        print(self.env_info)
        self.db[f"{self.config['env']['db_collection_name']}"].update_one({'_id': self.env_info_id}, {"$set":self.env_info})
        print("update check")
        cursor= self.db[f"{self.config['env']['db_collection_name']}"].find()
        for document in cursor:
            print(document)
        


    def int_trans(self):
        if self._cur_state == "MONITOR":
            self._cur_state = "MONITOR"
    
    #customize function name -> periodic get data -> 파라미터로
