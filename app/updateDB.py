import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import sqlite3
import json
from functions.configManager import config as createConfig, parent_dir

def scrape(dest_DB):
    #Get page HTML and create bs4 object
    URL = "https://www.e-cena.lv/"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    #Get both tables with prices
    tables=soup.find_all("table",class_="table")

    for n,t in enumerate(tables):
        #Get date of today and tommorow
        date=datetime.now()+timedelta(days=n)

        #Find all rows (price+time)
        rows=t.find_all("tr")
        for r in rows:
            #Seperate price and time
            items=r.findChildren("td" , recursive=False)
            if len(items)==2:
                #Convert and add to DB
                price=float(items[0].text)
                this_date=datetime.strptime(items[1].text, '%H:%M').replace(year=date.year, month=date.month,day=date.day)
                dest_DB.add(this_date.timestamp(),this_date.strftime('%d-%m-%Y'),this_date.strftime('%H:%M'),price)

def getTriggerTimes(this_DB,treshold_price):
    future_times=this_DB.getFuture()

    TT=[]
    state_old=False

    first=True
    for ft in future_times:
        state_new=(ft["price"]<treshold_price)
        state_display="ON" if state_new else "OFF"
        
        
        if state_new!=state_old or first:
            state_old=state_new
            TT.append([datetime.fromtimestamp(ft['timestamp']),state_display,state_new])
        
        first=False

    return TT

def saveTriggerTimes(times):
    with open("data/trigger_times.json","w") as f:
        json.dump(times,f)


def FullScanCheck(this_config, DB):
    last_scan=this_config.data["last_scan"]
    last_allowed=(datetime.now()-timedelta(hours=1)).timestamp()
    
    far_time=DB.getFarTime()
    this_time=datetime.now().timestamp()

    if far_time==None:
        return True
    if far_time<this_time:
        return True
    
    return last_scan<last_allowed




def main():
    config=createConfig()
    DB_path=f"{parent_dir}app/data/cenas.sqlite"

    DB=pricesDB(DB_path,"main")
    if FullScanCheck(config, DB):
        print("Running full scan")
        scrape(DB)
        DB.deleteOld()

        config.data["last_scan"]=(datetime.now()).timestamp()
        config.update()
    else:
        print("Running light scan")
    TT=getTriggerTimes(DB,config.data["treshold_price"])
    return TT

if __name__ == "__main__":
    main()

    
