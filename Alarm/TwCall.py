#!/usr/bin/env python3
import time
from twilio.rest import Client
from epics import caget
from influxdb import InfluxDBClient
import datetime
import urllib.request

def maincode():
    #Set your ip and port here:
    dbip='172.18.4.156'
    dbport='8086'

#Influx Database name:
    indb='AlarmDB'

#Defining database insert function:
    client=InfluxDBClient(host=dbip,port=dbport,database=indb)
    def influx(altype,iddet):
        timeset=datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        json_body = [
        {
            "measurement": "AlarmTable",
            "time": timeset,
            "fields": {
                "type":altype,
                "detno":iddet,
              }
          }]
        client.write_points(json_body)

#Initializing twilio parameters:
    account_sid="ACf0eb4d916265affb03fbbc391a151fbe"
    auth_token="7e11a7b8d07377554062b3d7819c292c"
    client=Client(account_sid,auth_token)

#Read alarm parameters from file:
    with open('/home/eliade/MAC-System-Grafana/GUI/Alarmconf.txt','r') as f:
        alarmlimits=f.read().split(',')
        for i in range(len(alarmlimits)):
            alarmlimits[i]=int(alarmlimits[i])
        callalarm=alarmlimits[0]

#Writing the call function:
    def twcall():
        call=client.calls.create(
            #these phone numbers are mine and my friends for testing. Do not run!
            to="+40725579088",
            from_="+40734260029",
            url="http://demo.twilio.com/docs/voice.xml"
            )
        print(call.sid)

#Monitoring for alarm triggers:
    while(True):
        DetTempValues = caget('172.18.4.108:EpicsLibrary:DetTempValues.VAL')
        for i in range(len(DetTempValues)):
            if DetTempValues[i]>=callalarm and DetTempValues[i]<100:
                twcall()
                influx('yellow',str(i+1))
                time.sleep(360)
                break

if __name__=="__main__":
    #Checking for internet connection
    while(True):
        def connect(host='http://google.com'):
            try:
                urllib.request.urlopen(host) #Python 3.x
                return True
            except:
                return False
        #If there is no internet connection SIMCall will run
        if connect():
            maincode()
        else:
            pass
