import requests,json

class PlugLan():
    def __init__(self,ip):
        self.ip=ip
        self.settings=self.get("settings")

    def isOn(self):
        return self.get("relay/0")["ison"]

    def turn(self,state:bool):
        if type(state)!=bool:
            return False

        command = "on" if state else "off"
        
        self.get(f"relay/0?turn={command}")
            
        return True
        
    def switch(self):
        self.turn(not(self.isOn()))
    def get(self,path):
        r=requests.get(f"http://{self.ip}/{path}")
        if r.status_code==200:
            self.connection=True
        else:
            self.connection=False
            raise Exception("Not 200")
        return r.json()
class PlugCloud:
    def __init__(self,server,API_key,device_id):
        self.server=server
        self.API_key=API_key
        self.device_id=device_id
    def get(self,path,payload={}):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        url=f"{self.server}/{path}"

        auth_payload={"id":self.device_id,"auth_key":self.API_key}
        payload = dict(payload, **auth_payload)
        payload_str="&".join([f"{key}={value}" for key, value in payload.items()])

        r = requests.request("POST", url, headers=headers, data=payload_str)

        
        if r.status_code==200:
            self.connection=True
        else:
            self.connection=False
            #raise Exception("Not 200")

        return r.json()


    def updateStatus(self):
        self.status=self.get("device/status")
    def isOn(self):
        self.updateStatus()
        return self.status['data']["device_status"]["relays"][0]["ison"]

    def turn(self,state:bool):

        if type(state)!=bool:
            return False

        command = "on" if state else "off"
        print(self.get("device/relay/control",{"channel":0,"turn":command}))

        return True

    def switch(self):
        self.turn(not(self.isOn()))




def connectPlug(connection,plug_config):
    if connection=="LAN":
        return PlugLan(plug_config["ip"])
    if connection=="CLOUD":
        return PlugCloud(plug_config["server"],plug_config["API"],plug_config["id"])


if __name__=="__main__":
    pass
