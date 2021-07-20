#!/usr/bin/env python3

import xml.etree.ElementTree as ET

#Make link to xml file:
xmltree=ET.parse('/home/eliade/MAC-System-Grafana/Control/ch_to_det_map.xml')
xmlroot=xmltree.getroot()

#Initialize xml file with zerores so we can modify with our inserted settings:
for x in xmlroot.findall('detector'):
    x.find('slot').text='0'
    x.find('channels').text='0'
xmltree.write('/home/eliade/MAC-System-Grafana/Control/ch_to_det_map.xml')

#Initializing inputs:
slotvec=[]
chvec=[]
detnr=input("Please enter the number of active detectors:")
for i in range(int(detnr)):
    a=input("Please enter the slot of Detector "+str(i+1)+":")
    b=input("Please enter the channels of the previous detector, separated by commas and no spaces ")
    slotvec.append(a)
    chvec.append(b)

#Writing into xml file:pyt
counter=0
for x in xmlroot.findall('detector'):
    x.find('slot').text=slotvec[counter]
    x.find('channels').text=chvec[counter]
    counter=counter+1
    if counter==int(detnr):
        break
xmltree.write('/home/eliade/MAC-System-Grafana/Control/ch_to_det_map.xml')