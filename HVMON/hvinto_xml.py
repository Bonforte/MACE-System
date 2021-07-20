#!/usr/bin/env python3

import xml.etree.ElementTree as ET
#1,12,4,8,7,8
#Make link to xml file:
xmltree=ET.parse('/home/eliade/MAC-System-Grafana/HVMON/HVConfiguration.xml')
xmlroot=xmltree.getroot()

#Initialize xml file with zerores so we can modify with our inserted settings:
for x in xmlroot.findall('board'):
    x.find('slot').text='0'
    x.find('chno').text='0'
xmltree.write('/home/eliade/MAC-System-Grafana/HVMON/HVConfiguration.xml')

#Initializing inputs:
slotvec=[]
chnovec=[]
brdnr=input("Please enter the number of active boards:")
for i in range(int(brdnr)):
    a=input("Please enter the slot number of the board with the number "+str(i+1)+":")
    b=input("Please enter the number of maximum channels of the board: ")
    slotvec.append(a)
    chnovec.append(b)

#Writing into xml file:pyt
counter=0
for x in xmlroot.findall('board'):
    x.find('slot').text=slotvec[counter]
    x.find('chno').text=chnovec[counter]
    counter=counter+1
    if counter==int(brdnr):
        break
xmltree.write('/home/eliade/MAC-System-Grafana/HVMON/HVConfiguration.xml')
