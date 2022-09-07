from datetime import  datetime

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