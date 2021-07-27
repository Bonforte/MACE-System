#!/usr/bin/env python3

from datetime import datetime
import time
from influxdb import InfluxDBClient
from epics import caget
import xml.etree.ElementTree as ET

#Declaring some constants that we will use:
epicsaddress='9b0ab43a3f7d7ff0'
#Set your ip and port here:
dbip='172.18.4.156'
dbport='8086'

#Influx Database name:
indb='HVMonitor'

#Influx measurement name:
inm="HVMONDB"

#InfluxDB setup:
client=InfluxDBClient(host=dbip,port=dbport,database=indb)
clientDet=InfluxDBClient(host=dbip,port=dbport,database=indb)

#Seeing what is active using configuration file
slotvec=[]
channelsvec=[]
xmltree=ET.parse('/home/eliade/MAC-System-Grafana/HVMON/HVConfiguration.xml')
xmlroot=xmltree.getroot()
for x in xmlroot.findall('board'):
    slot=x.find('slot').text
    slot=int(slot)
    channels=x.find('chno').text
    channels=int(channels)
    slotvec.append(slot)
    channelsvec.append(channels)

#Deleting 0 values for better efficiency of alarm trigger
channelsvecdel=[]
slotvecdel=[]
for i in range(len(channelsvec)):
    if channelsvec[i]==0:
        channelsvecdel.append(i)
cntr=0
for ch in channelsvecdel:
    channelsvec.remove(channelsvec[ch-cntr])
    cntr=cntr+1

for x in range(len(slotvec)):
    if slotvec[x]==0:
        slotvecdel.append(x)
cntr=0
for sl in slotvecdel:
    slotvec.remove(slotvec[sl-cntr])
    cntr=cntr+1
print(channelsvec,slotvec)

#Printing working slots for insight:
print("\n\nActive slots with respective channels:\n")
for i in range(0,len(slotvec)):
    print("Slot "+str(slotvec[i])+" with the number of channels being: "+str(channelsvec[i])+";")
    print("-------------------------------------------")

#Reading waiting time between read-outs:
with open('/home/eliade/MAC-System-Grafana/GUI/wait_time.txt','r') as f:
    wtime=int(f.read())
print("\nThe waiting time between read-outs is : "+ str(wtime)+" seconds.")

#Initializing the lists that will store the monitoring data during the code:
resultV=[]
resultI=[]

#Run the monitoring:
while(1):
    timeset=datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    for j in range(len(slotvec)):
        for x in range(channelsvec[j]):
            m1=caget(epicsaddress+':'+str(slotvec[j]).zfill(2).zfill(2)+':'+str(x).zfill(3)+':VMon')
            resultV.append(m1)
            m2=caget(epicsaddress+':'+str(slotvec[j]).zfill(2)+':'+str(x).zfill(3)+':IMon')
            resultI.append(m2)
        m3=caget(epicsaddress+':'+str(slotvec[j]).zfill(2)+':Temp')
        resultT=m3
        json_bodyboard=[
            {
            "measurement": inm,
            "time":timeset,
            "fields":
            {
                "temp"+str(slotvec[j]):resultT
            }
            }
        ]
        for y in range(channelsvec[j]):
            json_bodyboard.append(
               {
            "measurement": inm,
            "time":timeset,
            "fields":
            {
                "VMon"+str(slotvec[j])+'|'+str(y+1):resultV[y]
            }
            }
            )
            json_bodyboard.append(
               {
            "measurement": inm,
            "time":timeset,
            "fields":
            {
                "IMon"+str(slotvec[j])+'|'+str(y+1):resultI[y]
            }
            }
            )
        client.write_points(json_bodyboard)
        resultV=[]
        resultI=[]
        resultT=0
    time.sleep(wtime)



        
