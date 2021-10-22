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

newIp = '172.18.4.108'

#Influx Database name:
indb='AlarmDB'

#Influx measurement name:
inm="AlarmTable"

#Defining database insert function:
client=InfluxDBClient(host=dbip,port=dbport,database=indb)
def influx(altype,iddet):
    timeset=datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    json_body = [
        {
            "measurement": inm,
            "time": timeset,
            "fields": {
                "type":altype,
                "detno":iddet,
              }
          }]
    client.write_points(json_body)

#Initializing arrays that we will need:
slotvec=[]
channelsvec=[]
idvec=[]
ConfDet=[]
DetTempMatrix=[]
avgvec=[]

#Parsing XML file:
xmltree=ET.parse('/home/eliade/MAC-System-Grafana/Control/ch_to_det_map.xml')
xmlroot=xmltree.getroot()
for x in xmlroot.findall('detector'):
    slot=x.find('slot').text
    id=x.find('id').text
    channels=x.find('channels').text
    channels=channels.split(",")
    for i in range(len(channels)):
        if channels[i]!='0':
            channels[i]=int(channels[i])
            channels[i]=channels[i]-1
            channels[i]=str(channels[i])
    for i in range(len(channels)):
        channels[i]=channels[i].zfill(3)
    slotvec.append(slot.zfill(2))
    idvec.append(int(id))
    channelsvec.append(channels)

#Deleting 0 values for better efficiency of alarm trigger
channelsvecdel=[]
slotvecdel=[]
idvecdel=[]
for i in range(len(channelsvec)):
    if channelsvec[i][0]=='000':
        channelsvecdel.append(i)
cntr=0
for ch in channelsvecdel:
    channelsvec.remove(channelsvec[ch-cntr])
    cntr=cntr+1

for x in range(len(slotvec)):
    if slotvec[x]=='00':
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


#Reading alarm limits:
with open('/home/eliade/MAC-System-Grafana/GUI/Alarmconf.txt','r') as f:
    alarmlimits=f.read().split(',')
    for i in range(len(alarmlimits)):
        alarmlimits[i]=int(alarmlimits[i])
sdalarm=alarmlimits[-1]
tfalarm=alarmlimits[-2]

#Monitoring for trigger signs:
while(True):
    #forming a matrix of 10 values on each temperature index for better monitoring
    for i in range(10):
        DetTempValues = caget('172.18.4.108:EpicsLibrary:DetTempValues.VAL')
        DetTempMatrix.append(DetTempValues)
        time.sleep(3)
    #resetting working arrays
    avgvec=[]
    ConfDet=[]
    #calculating the average of those 10 values for each temperature index
    for r in range(len(DetTempValues)):
        sum=0
        for p in range(len(DetTempMatrix)):
            sum+=DetTempMatrix[p][r]
        avgvec.append(sum/len(DetTempMatrix))
    for z in range(len(avgvec)):
        if avgvec[z]>=sdalarm:
            for id in range(len(idvec)):
                if idvec[id]==z+1:
                    print("Shutdown alarm!")
                    for x in range(len(channelsvec[id])):
                        caput('9b0ab43a3f7d7ff0:'+str(slotvec[id])+':'+str(channelsvec[id][x])+':Pw',0)
                    influx('red',str(z+1))
                    ConfDet.append(z+1)                
        if avgvec[z]>=tfalarm and avgvec[z]<100:
            print('Trigger filling alarm!')
            influx('tfill',str(z+1))
            time.sleep(360)
    if(ConfDet):
        time.sleep(1200)
        for id in range(len(idvec)):
            if idvec[id] in ConfDet :
                for x in range(len(channelsvec[id])):
                    caput('9b0ab43a3f7d7ff0:'+str(slotvec[id])+':'+str(channelsvec[id][x])+':Pw',1)