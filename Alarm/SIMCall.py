#!/usr/bin/env python3

import time
from ppadb.client import Client as AdbClient
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

#Read alarm parameters from file:
    with open('/home/eliade/MAC-System-Grafana/GUI/Alarmconf.txt','r') as f:
        alarmlimits=f.read().split(',')
        for i in range(len(alarmlimits)):
            alarmlimits[i]=int(alarmlimits[i])
    callalarm=alarmlimits[0]

    def connect():
        client=AdbClient(host="127.0.0.1", port=5037)
        devices=client.devices()
        if len(devices)==0:
            print('No devices')
            quit()
        device=devices[0]
        print(f'Connected to {device}')
        return device,client

    def initialize():
        device,client=connect()
        device.shell('adb -s device shell am start -a android.intent.action.CALL -d tel:+40734260029')

    #Monitoring for alarm triggers:
    while(True):
        DetTempValues = caget('172.18.4.108:EpicsLibrary:DetTempValues.VAL')
        for i in range(len(DetTempValues)):
            if DetTempValues[i]>=callalarm and DetTempValues[i]<100:
                initialize()
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
            pass
        else:
            maincode()

#sudo adb start-server