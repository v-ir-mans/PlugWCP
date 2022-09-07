

import requests
from bs4 import BeautifulSoup
from datetime import datetime,timedelta

def scrape():
    #Get page HTML and create bs4 object
    URL = "https://www.e-cena.lv/"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    #Get both tables with prices
    tables=soup.find_all("table",class_="table")

    return_list=[]
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
                return_list.append([this_date,price])
    return return_list

def updateDB(this_DB, data):
    for d in data:
        time=d[0]
        price=d[1]
        this_DB.add(time.timestamp(),time.strftime('%d-%m-%Y'),time.strftime('%H:%M'),price)

def fullScanCheck(this_config, DB):
    last_scan=this_config.data["last_scan"]
    last_allowed=(datetime.now()-timedelta(hours=1)).timestamp()
    
    far_time=DB.getFarTime()
    this_time=datetime.now().timestamp()

    if far_time==None:
        return True
    if far_time<this_time:
        return True
    
    return last_scan<last_allowed

def main(config, pricesDB):

    if not(fullScanCheck(config, pricesDB)):
        return False

    scrape_data=scrape()
    updateDB(pricesDB, scrape_data)
    
    config.data["last_scan"]=(datetime.now()).timestamp()
    config.update()
    
    pricesDB.deleteOld()

    return True

