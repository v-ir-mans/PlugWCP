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

#Code itself 
config=createConfig()

from scraping import main as scrapeAndUpdateDB
scrape_result=scrapeAndUpdateDB()
if scrape_result:
    print("Completed full scan")
else:
    print("Full scan was not needed")
