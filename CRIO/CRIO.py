#!/usr/bin/env python3

from influxdb import InfluxDBClient
from datetime import datetime
import time
from epics import caget

#Set your ip and port here:
dbip='172.18.4.156'
dbport='8086'

#Influx Database name:
indb='CRIO'

#InfluxDB setup:
client=InfluxDBClient(host=dbip,port=dbport,database=indb)
clientDet=InfluxDBClient(host=dbip,port=dbport,database=indb)
# Globals
DetTempValues=[]
valvesTempValues=[]


def main():


  while (1):


    try:
      DetTempValues = caget('172.18.4.108:EpicsLibrary:DetTempValues.VAL')
      valvesTempValues =caget('172.18.4.108:EpicsLibrary:ValvesTempValues.VAL')
      #print(DetTempValues[:])
      #print(valvesTempValues[:])

    except Exception as e: # work on python 3.x
      print('Failed to caget: '+ str(e))
      detTemperatures=f"{('Data N/A, at ' + datetime.now().strftime('%H:%M:%S')):^120}"
      valvesTemperatures=f"{'----------------,   ':^120}"
    timeset=datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    json_bodyValv = [
        {
            "measurement": "CoolingSystemValves",
            "time": timeset,
            "fields": {
                "temp1":valvesTempValues[0]
              }
          },
        {
            "measurement": "CoolingSystemValves",
            "time": timeset,
            "fields": {
                "temp2":valvesTempValues[1]
              }
           },
        {
            "measurement": "CoolingSystemValves",
            "time": timeset,
            "fields": {
                "temp3":valvesTempValues[2]
              }
          },
        {
            "measurement": "CoolingSystemValves",
            "time": timeset,
            "fields": {
                "temp4":valvesTempValues[3]
              }
          },
        {
            "measurement": "CoolingSystemValves",
            "time": timeset,
            "fields": {
                "temp5":valvesTempValues[4]
              }
          },
        {
            "measurement": "CoolingSystemValves",
             "time": timeset,
            "fields": {
                "temp6":valvesTempValues[5]
              }
          },
        {
            "measurement": "CoolingSystemValves",
            "time": timeset,
            "fields": {
                "temp7":valvesTempValues[6]
              }
          },
        {
            "measurement": "CoolingSystemValves",
            "time": timeset,
            "fields": {
                "temp8":valvesTempValues[7]
              }
          },
        {
            "measurement": "CoolingSystemValves",
            "time": timeset,
            "fields": {
                "temp9":valvesTempValues[8]
              }
          },
        {
            "measurement": "CoolingSystemValves",
            "time": timeset,
            "fields": {
                "temp10":valvesTempValues[9]
              }
          }

      ]
  
    json_bodyDet = [
        {
            "measurement": "CoolingSystemDet",
            "time": timeset,
            "fields": {
                "temp1":DetTempValues[0]
              }
          },
        {
            "measurement": "CoolingSystemDet",
            "time": timeset,
            "fields": {
                "temp2":DetTempValues[1]
              }
           },
        {
            "measurement": "CoolingSystemDet",
            "time": timeset,
            "fields": {
                "temp3":DetTempValues[2]
              }
          },
        {
            "measurement": "CoolingSystemDet",
            "time": timeset,
            "fields": {
                "temp4":DetTempValues[3]
                }
          },
        {
            "measurement": "CoolingSystemDet",
            "time": timeset,
            "fields": {
                "temp5":DetTempValues[4]
              }
          },
        {
            "measurement": "CoolingSystemDet",
            "time": timeset,
            "fields": {
                "temp6":DetTempValues[5]
              }
          },
        {
            "measurement": "CoolingSystemDet",
            "time": timeset,
            "fields": {
                "temp7":DetTempValues[6]
              }
          },
        {
            "measurement": "CoolingSystemDet",
            "time": timeset,
            "fields": {
                "temp8":DetTempValues[7]
              }
          }
        ]

    clientDet.write_points(json_bodyDet)
    client.write_points(json_bodyValv)
    
    time.sleep(2)

if __name__ == '__main__':

  main()




