from functions.configManager import config as createConfig, parent_dir
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

sys.stdout = Logger(f"{parent_dir}app/data/output.log")

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

############################################
#Code itself 

config=createConfig()

from functions.shellyPlug import connectPlug
def createPlug(config):
    con_type=config.data["plug"]["connection"]
    return connectPlug(con_type,config.data["plug"][con_type])
maija=createPlug(config)

def turnLights(state, plug):
    plug.turn(state)
    print(state)


from functions.pricesDBmanager import pricesDB as createPricesDB
pricesDB=createPricesDB(f"{parent_dir}app/data/cenas.sqlite","main")



import functions.triggerTimes as TTfunc
TT_manager=TTfunc.manager(turnLights)
TT_manager.initiate()

from functions.scraping import main as scrapeAndUpdateDB
def scan(recalc_TT=False):



    print("Running regular scan")
    scrape_result=scrapeAndUpdateDB(config,pricesDB)
    if scrape_result:
        recalc_TT=True
    if recalc_TT:
        print("Recalculating TT")
        trigger_times=TTfunc.getTriggerTimes(pricesDB,config.data["treshold_price"])
        false_trigger_times=TTfunc.genPereodicalTime(8,10)
        TTfunc.displayTT(trigger_times)
        
        TT_manager.clearPlan()
        for TT in trigger_times:
            TT_manager.newTT(TT[0],[TT[2],maija])
    else:
        print("TT recalculation wasn't needed")



from apscheduler.schedulers.background import BackgroundScheduler

scraping_scheduler=BackgroundScheduler(timezone="Europe/Riga")
scraping_scheduler.add_job(scan,trigger="interval",seconds=config.data["regular_scan_interval"],id="scan")
scraping_scheduler.start()
scan(True)



while True:
    if config.hasChanged():

        print(">Spotted change")
        config.load()
        scan(True)