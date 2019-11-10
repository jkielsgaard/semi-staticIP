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
        fr = open(fil, "r")
        content = fr.read()
        fr.close()
        if not (content == ip):
                RewriteFile(ip, fil)
                return True
        else:
                return False

def RewriteFile(ip, fil):
        fw = open(fil,"w+")
        fw.write(ip)
        fw.close()
#####

# Check for folder and files
def CheckFolderExist(folder):
        if not os.path.isdir(folder):
                os.mkdir(folder)

def CheckFileExist(fil):
        if not os.path.isfile(fil):
                fw = open(fil,"w+")
                fw.close()
#####

# Creates logs
def Log(log, path):
        path = "log"
        CheckFolderExist(path)
        now = datetime.now()
        date = now.strftime("%Y%m%d")
        time = now.strftime("%H:%M:%S")
        fil = path + "/" + date + ".log"
        CheckFileExist(fil)
        fa = open(fil, "a+")
        fa.write(time + " - " + log + "\r\n")
        fa.close
#####

# Get file content
def GetContent(fil):
        fr = open(fil, "r")
        content = fr.read().splitlines()
        fr.close()
        return content[0]
#####

# Running script
def RUN():
        keyFile = "KEY.txt"
        UrlFile = "Url.txt"
        wanipFile = "WanIP.txt"
        LogFolder = "log"

        CheckFileExist(wanipFile)
        CheckFileExist(keyFile)
        CheckFileExist(UrlFile)
        CheckFolderExist(LogFolder)

        key = GetContent(keyFile)
        url = GetContent(UrlFile)
        if not url == "":
                if not key == "":
                        ip = GetWanIP()

                        if not ip == "NULL":
                                if CheckWanIP(ip, wanipFile) == True:
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