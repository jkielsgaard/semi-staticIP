import requests
import json
import time
import os
from datetime import datetime

# Getting and updating WANIP
def APIPost(ip, url, key):
        data = json.dumps(ip)
        headers = {'content-type': 'application/json', 'x-api-key': '' + key + ''}

        response = requests.post(url, data=data, headers=headers)
        return response.text

def GetWanIP():
        content = ""
        try:    
                content = requests.get('https://checkip.amazonaws.com').text.strip()
        except: 
                content = "NULL"
        return  content

def CheckWanIP(ip, fil):
        key = GetJsonData(fil, 'WanIP')

        if not (key == ip):
                UpdateWanIP(fil, ip)
                return True
        else:
                return False
###########################

# Json Workers
def CreateJsonFile(fil): 
        os.mknod(fil)
        data = { 'url': '', 'apikey': '', 'WanIP': '' }
        with open(fil, 'w') as outfile:
                json.dump(data, outfile)

def GetJsonData(fil, key):
        with open(fil) as json_file:
                data = json.load(json_file)
                return data[key]

def UpdateWanIP(fil, ip):
        with open(fil) as json_file:
                data = json.load(json_file)
        
        Newdata = { 'url': data['url'], 'apikey': data['apikey'], 'WanIP': ip }

        with open(fil, 'w') as outfile:
                json.dump(Newdata, outfile)
###########################


# Creates logs
def Log(log):
        now  = datetime.now()
        date = now.strftime("%Y%m%d")
        time = now.strftime("%H:%M:%S")


        logFile = "/opt/autohomeip/log/" + date + ".log"
        if not os.path.isfile(logFile):
                os.mknod(logFile)
        
        fa = open(logFile, "a+")
        fa.write(time + " - " + log + "\r\n")
        fa.close
###########################

# Running script
def RUN():
        jsonFile = "/opt/autohomeip/config/data.json"

        if not os.path.isfile(jsonFile):
                CreateJsonFile(jsonFile)

        key = GetJsonData(jsonFile, 'apikey')
        url = GetJsonData(jsonFile, 'url')
        if not url == "":
                if not key == "":
                        ip = GetWanIP()

                        if not ip == "NULL":
                                if CheckWanIP(ip, jsonFile) == True:
                                        Log(APIPost(ip, url, key))
                                        Log("API CALL - WANIP: " + ip)
                                else:
                                        Log("NO CHANGE")
                        else: 
                                Log("CONNECTIONS ERROR")
                else:
                        Log("APIKEY ERROR")
        else:
                Log("URL ERROR")

RUN()