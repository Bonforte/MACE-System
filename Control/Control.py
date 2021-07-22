#!/usr/bin/env python3

from epics import caput,caget
import xml.etree.ElementTree as ET
from influxdb import InfluxDBClient
from datetime import datetime
import time

#HV Adress
epicsaddress='9b0ab43a3f7d7ff0'

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

#Parsing XML file:
slotvec=[]
channelsvec=[]
idvec=[]
xmltree=ET.parse('/home/eliade/MAC-System-Grafana/Control/ch_to_det_map.xml')
xmlroot=xmltree.getroot()
for x in xmlroot.findall('detector'):
    slot=x.find('slot').text
    id=x.find('id').text
    channels=x.find('channels').text
    channels=channels.split(",")
    
    slotvec.append(int(slot))
    idvec.append(int(id))
    for i in range(len(channels)):
        channels[i]=int(channels[i])
    channelsvec.append(channels)

#Deleting 0 values for better efficiency of alarm trigger
channelsvecdel=[]
slotvecdel=[]
idvecdel=[]
for i in range(len(channelsvec)):
    if channelsvec[i][0]==0:
        channelsvecdel.append(i)
cntr=0
for ch in channelsvecdel:
    channelsvec.remove(channelsvec[ch-cntr])
    cntr=cntr+1

for x in range(len(slotvec)):
    if slotvec[x]==0:
        slotvecdel.append(x)
        idvecdel.append(x)
cntr=0
for sl in slotvecdel:
    slotvec.remove(slotvec[sl-cntr])
    cntr=cntr+1
cntr=0
for id in idvecdel:
    idvec.remove(idvec[id-cntr])
    cntr=cntr+1
print(channelsvec,slotvec,idvec)

#Reading alarm limits:
with open('/home/eliade/MAC-System-Grafana/GUI/Alarmconf.txt','r') as f:
    alarmlimits=f.read().split(',')
    for i in range(len(alarmlimits)):
        alarmlimits[i]=int(alarmlimits[i])
sdalarm=alarmlimits[-1]
tfalarm=alarmlimits[-2]

#Monitoring for trigger signs:
#slotvec and channelsvec needed for shutdown signal
while(True):
    for i in range(len(slotvec)):
        for j in range(len(channelsvec)):
            DetTempValues = caget('172.18.4.108:EpicsLibrary:DetTempValues.VAL')
            for z in range(len(DetTempValues)):
                if DetTempValues[z]>=sdalarm and DetTempValues[z]<tfalarm:
                    print("Shutdown initiated!")
                    influx('red',str(z+1))
                    time.sleep(360)
                if DetTempValues[z]>=tfalarm and DetTempValues[z]<100:
                    print('Trigger filling initiated!')
                    influx('tfill',str(z+1))
                    time.sleep(360)


#caput('9b0ab43a3f7d7ff0:01:000:Pw',1)
