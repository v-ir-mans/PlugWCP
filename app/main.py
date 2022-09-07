import sys

class Logger(object):
    def __init__(self, path):
        self.terminal = sys.stdout
        self.path=path
        self.file = open(self.path, "w")
   
    def write(self, message):
        self.terminal.write(message)
        self.file.write(message)  
        self.flush()


    def flush(self):
        self.file.flush()

sys.stdout = Logger("assets/data/output.log")


print("""  _____  _          __          _______ _____  
 |  __ \| |         \ \        / / ____|  __ \ 
 | |__) | |_   _  __ \ \  /\  / / |    | |__) |
 |  ___/| | | | |/ _` \ \/  \/ /| |    |  ___/ 
 | |    | | |_| | (_| |\  /\  / | |____| |     
 |_|    |_|\__,_|\__, | \/  \/   \_____|_|     
                  __/ |                        
                 |___/                         
""")

#Stop loop when CTRL+C is pressecd
import signal
def signal_handler(sig, frame):
    print("\n Program stopped")
    exit()
signal.signal(signal.SIGINT, signal_handler)

#Code itself  |
#            \ /
#             V


#imports config dictionary
import assets.functions.config as fc
config=fc.config()

#Imports and creates Shelly plug
from assets.functions.shelly_plug import connectPlug
def createPlug(this_config):
    con_type=this_config.data["plug"]["connection"]
    return connectPlug(con_type,this_config.data["plug"][con_type])

maija=createPlug(config)

def switchPlug(state):
    print(f"Change plug to {state}")
    maija.turn(state)

#Gets trigger times
from updateDB import main as getTT
real_trigger_times=getTT()


#Creates empty trigger time manager
import assets.functions.trigger_times as trigger_times
gen_trigger_times=trigger_times.genTT(len=5,sec=5)

TT_manager=trigger_times.triger_times_manager(switchPlug,real_trigger_times)
TT_manager.initiate()


while True:
    if config.hasChanged():
        
        print("Spotted change")

        #update all
        #--update config
        config.load()
        #--update plug
        maija=createPlug(config)
        #--update trigger times
        real_trigger_times=getTT()
        gen_trigger_times=trigger_times.genTT(len=5,sec=5)
        TT_manager.createPlan(real_trigger_times)

