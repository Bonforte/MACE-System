#!/usr/bin/env python3

from datetime import datetime
import time
from influxdb import InfluxDBClient
from epics import caget

#Declaring some constants that we will use:
epicsaddress='9b0ab43a3f7d7ff0'
client=InfluxDBClient(host='172.18.4.156',port='8086',database='HVMonitor')

#Seeing what is active using configuration file
conf_list=[]
conf_ch=[]
conf_slots=[]
with open('HVConfiguration.conf','r') as f:
    line_data=f.readline()
    conf_list=line_data.split(',')

#Converting vector strings to integers to be used
for i in range(len(conf_slots)):
    conf_list[i]=int(conf_list[i])

#Dividing numbers from configuration list into slots and channels:
for i in range(0,len(conf_list),2):
    conf_slots.append(int(conf_list[i]))
    conf_ch.append(int(conf_list[i+1]))

print(conf_slots)
print(conf_ch)
#Printing working slots for insight:
print("\n\nActive slots with respective channels:\n")
for i in range(0,len(conf_slots)):
    print("Slot "+str(conf_slots[i])+" with the number of channels being: "+str(conf_ch[i])+";")
    print("-------------------------------------------")

#Reading waiting time between read-outs:
with open('/GUI/wait_time.txt','r') as f:
    wtime=int(f.read())
print("\nThe waiting time between read-outs is : "+ str(wtime)+" seconds.")

#Initializing the lists that will store the monitoring data during the code:
resultV=[]
resultI=[]

#Run the monitoring:
while(1):
    timeset=datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    for j in range(len(conf_slots)):
        for x in range(conf_ch[j]):
            if x>=10:
                if conf_slots[j]>=10:
                    m1=caget(epicsaddress+':'+str(conf_slots[j])+':0'+str(x)+':VMon')
                else:
                    m1=caget(epicsaddress+':'+'0'+str(conf_slots[j])+':0'+str(x)+':VMon')
            else:
                if conf_slots[j]>=10:
                    m1=caget(epicsaddress+':'+str(conf_slots[j])+':00'+str(x)+':VMon')
                else:
                    m1=caget(epicsaddress+':'+'0'+str(conf_slots[j])+':00'+str(x)+':VMon')
            resultV.append(m1)
            if x>=10:
                if conf_slots[j]>=10:
                    m2=caget(epicsaddress+':'+str(conf_slots[j])+':0'+str(x)+':IMon')
                else:
                    m2=caget(epicsaddress+':'+'0'+str(conf_slots[j])+':0'+str(x)+':IMon')
            else:
                if conf_slots[j]>=10:
                    m2=caget(epicsaddress+':'+str(conf_slots[j])+':00'+str(x)+':IMon')
                else:
                    m2=caget(epicsaddress+':'+'0'+str(conf_slots[j])+':00'+str(x)+':IMon')
            resultI.append(m2)
        if conf_slots[j]>=10:
            m3=caget(epicsaddress+':'+str(conf_slots[j])+':Temp')
        else:
            m3=caget(epicsaddress+':'+'0'+str(conf_slots[j])+':Temp')
        resultT=m3
        json_bodyboard=[
            {
            "measurement": "HVMONDB",
            "time":timeset,
            "fields":
            {
                "temp"+str(conf_slots[j]):resultT
            }
            }
        ]
        client.write_points(json_bodyboard)
        for y in range(conf_ch[j]):
            json_bodyboard.append(
               {
            "measurement": "HVMONDB",
            "time":timeset,
            "fields":
            {
                "VMon"+str(conf_slots[j])+'|'+str(y+1):resultV[y]
            }
            }
            )
            json_bodyboard.append(
               {
            "measurement": "HVMONDB",
            "time":timeset,
            "fields":
            {
                "IMon"+str(conf_slots[j])+'|'+str(y+1):resultI[y]
            }
            }
            )
        client.write_points(json_bodyboard)
        resultV=[]
        resultI=[]
        resultT=0
    time.sleep(wtime)



        
