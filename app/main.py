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

def turnLights(state):
    print(8*"-"+"Lights go brr and " + state)


from functions.pricesDBmanager import pricesDB as createPricesDB
pricesDB=createPricesDB(f"{parent_dir}app/data/cenas.sqlite","main")



import functions.triggerTimes as TT
TT_manager=TT.manager(turnLights)
TT_manager.initiate()

from functions.scraping import main as scrapeAndUpdateDB
def scan(recalc_TT=False):
    print("Running regular scan")
    scrape_result=scrapeAndUpdateDB(config,pricesDB)
    if scrape_result:
        recalc_TT=True
    if recalc_TT:
        print("Recalculating TT")
        trigger_times=TT.getTriggerTimes(pricesDB,config.data["treshold_price"])
        false_trigger_times=TT.genPereodicalTime(8,3)
        TT.displayTT(false_trigger_times)
        
        TT_manager.createPlan(false_trigger_times)
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
        scan(TT)