from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from time import sleep


class manager:
    def __init__(self, target_function,TT_list=[] ):
        self.sheduler=BackgroundScheduler(timezone="Europe/Riga")
        self.target_func=target_function
        self.createPlan(TT_list)
    def initiate(self):
        self.sheduler.start()
    def clearPlan(self):
        self.sheduler.remove_all_jobs()
    def createPlan(self,new_TT_list):
        self.clearPlan()
        for TT in new_TT_list:
            self.sheduler.add_job(self.target_func,'date',run_date=(TT[0]),args=[TT[1]], misfire_grace_time=None)
        self.TT_list=new_TT_list


def genPereodicalTime(len=5, sec=3):
    return_list=[]
    time_now=datetime.now()
    for i in range(len):
        timestamp=(time_now+timedelta(seconds=(i+1)*sec))
        if not(i%2):
            return_list.append([timestamp, "ON", True])
        else:
            return_list.append([timestamp, "OFF", False])
    return return_list

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

def displayTT(TT_list):
    for TT in TT_list:
        print(f"Turn {TT[1]} at {TT[0].strftime('%H:%M:%S')} ")