from pyevsim.system_simulator import SystemSimulator
from pyevsim.behavior_model_executor import BehaviorModelExecutor
from pyevsim.definition import *

class DTemplate(BehaviorModelExecutor):
    pass

class PeriodicDataCollector(DTemplate):
    def __init__(self, inst_t, dest_t, mname, ename, obj):
        super().__init__(inst_t, dest_t, mname, ename)

        self.init_state("Wait")
        self.insert_state("Wait", Infinite)
        self.insert_state("Generate",1)
        self.obj = obj

        self.insert_input_port("start")
    def ext_trans(self,port, msg):
        pass
    
    def output(self):
        pass
    
    def int_trans(self):
        pass
#UDO MODEL
from UDO import WeatherCollection

#NETWORK MODEL
#from NetworkMOdel.() import ()

#REGISTER SIMULATION ENGINE (Engine Name, Mode, Engine Operation Period) 
ss = SystemSimulator()
ss.register_engine("first", "REAL_TIME", 1)

#CREATE ENGINE INPUT PORT
ss.get_engine("first").insert_input_port("start")

#DEFINE DES MODEL(CLASS)
gen = PeriodicDataCollector(0, Infinite, "Gen", "first", WeatherCollection())

#REGISTER DES MODEL WITH THE ENGINE
ss.get_engine("first").register_entity(gen)

#COUPLING BETWEEN PORT(MODEL_N, MODEL_N_PORT, MODEL_M,MODEL_M_PORT)
ss.get_engine("first").coupling_relation(None, "start", gen, "start")

#INSERT EXTERNAL EVENT(PORT, ENGINE)
ss.get_engine("first").insert_external_event("start", None)

#SIMULATION OPERATION
ss.get_engine("first").simulate()