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


# Check of create folder and files
def CheckFolderExist(folder): 
        if os.path.isdir(folder):
                return True
        else:
                return False

def CreateFolder(folder):
        os.mkdir(folder)

def CheckFileExist(fil):
        if os.path.isfile(fil):
                return True
        else:
                return False

def CreateFile(fil):
        os.mknod(fil)
###########################

# Creates logs
def Log(log, path):
        path = "log"
        now  = datetime.now()
        date = now.strftime("%Y%m%d")
        time = now.strftime("%H:%M:%S")
        
        if not CheckFolderExist(path):
                CreateFolder(path)

        fil = path + "/" + date + ".log"
        if not CheckFileExist(fil):
                CreateFile(fil)
        
        fa = open(fil, "a+")
        fa.write(time + " - " + log + "\r\n")
        fa.close
###########################

# Running script
def RUN():
        Jsonfile = "data.json"
        LogFolder = "log"

        if not CheckFileExist(Jsonfile):
                CreateJsonFile(Jsonfile)

        CheckFolderExist(LogFolder)

        key = GetJsonData(Jsonfile, 'apikey')
        url = GetJsonData(Jsonfile, 'url')
        if not url == "":
                if not key == "":
                        ip = GetWanIP()

                        if not ip == "NULL":
                                if CheckWanIP(ip, Jsonfile) == True:
                                        Log(APIPost(ip, url, key), LogFolder)
                                        Log("API CALL - WANIP: " + ip, LogFolder)
                                else:
                                        Log("NO CHANGE", LogFolder)
                        else: 
                                Log("CONNECTIONS ERROR", LogFolder)
                else:
                        Log("APIKEY ERROR", LogFolder)
        else:
                Log("URL ERROR", LogFolder)

RUN()