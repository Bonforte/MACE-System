#!/usr/bin/env python3
import redis
import json
import time


#Initializing connection with database

with open("/home/eliade/Desktop/MACE-System/RMACE/Confjson/db_config_settings.json","r") as db_json:
    json_object=json.load(db_json)
    
host=json_object["Credentials"]["redis_ip"]
port=json_object["Credentials"]["redis_port"]
db=json_object["Credentials"]["redis_db_no"]

redb=redis.Redis(host,port,db)

#Defining limit functions

def Check_in_Limits(a,c,d,edge):
    if float(a)>(float(c)+edge) and float(a)<=(float(d)-edge):
        return True
    else:
        return False

def Check_out_Limits(a,c,d):
    if float(a)<float(c) and float(a)>float(d):
        return True
    else:
        return False

def CheckAlarmCond(detector, attrs, detaljson, edge_array,trigger, detmonjson, cond_no):
    index = int(detector[-1])-1


    #Checking for basic alarm levels
    for condition in range(1,cond_no+1):

        if Check_in_Limits(detmonjson["CurrentTemp"][index],attrs["Condition "+str(condition)][0],attrs["Condition " + str(condition)][1],edge_array[condition-1]):
            detaljson[detector]["Triggers"][condition-1]+=1
            
            if detaljson[detector]["Triggers"][condition-1]>=trigger:
                detaljson[detector]["AlarmLevel"] = condition
                

                for z in range(len(detaljson[detector]['Triggers'])):
                    if detaljson[detector]["Triggers"][z] != detaljson[detector]["Triggers"][condition-1]:
                        if detaljson[detector]["Triggers"][z] > 0:
                            detaljson[detector]["Triggers"][z] -= 1

    #Checking for special cases
                            
    #No alarms
    if Check_out_Limits(detmonjson["CurrentTemp"][index],attrs["Condition 1"][0],attrs["Condition 4"][1]):
        if detaljson[str(detector)]['Triggers'][4]>=trigger:
            
            detaljson[detector]['AlarmLevel']=0
            
            for z in range(len(detaljson[str(detector)]['Triggers'])):
                if z != 4 :
                    if detaljson[detector]["Triggers"][z] > 0:
                        detaljson[detector]["Triggers"][z] -= 1

    #disconnected:
    elif float(detmonjson["CurrentTemp"][index])>100:
        
        detaljson[detector]['AlarmLevel']='dc'
        for z in range(len(detaljson[str(detector)]['Triggers'])):
            if z != 5 :
                if detaljson[detector]["Triggers"][z] > 0:
                    detaljson[detector]["Triggers"][z] -= 1

    redb.watch("Detectors_Alarms")
    redjson=json.dumps(detaljson,ensure_ascii=False).encode('utf-8')
    redb.set('Detectors_Alarms',redjson)

    redb.watch("Monitoring_Data")
    redjson=json.dumps(detmonjson,ensure_ascii=False).encode('utf-8')
    redb.set('Monitoring_Data',redjson)
    

#Defining main function
                            
def Control(stop):
    inMemDb=redb.exists('Detectors_Alarms')


    try:
        if(inMemDb):
            while(True):
                time.sleep(2)
                
                #Load redis into json
                detcnfgjson=json.loads(redb.get("Detectors_config").decode("utf-8"))

                detaljson=json.loads(redb.get("Detectors_Alarms").decode("utf-8"))

                detmonjson=json.loads(redb.get("Monitoring_Data").decode("utf-8"))
                
                #Recording detectors that were activated for monitorization in local array:
                detlist=[]
                for detector,attrs in detcnfgjson.items():
                    if attrs['MonVar']:
                        detlist.append(str(detector))

                #Comparing for alerts;
                for detector,attrs in detcnfgjson.items():
                    
                    if detector in detlist:
                        trigger=detcnfgjson[str(detector)]['TriggerTime']

                        #Recording detector index for data structure access:
                        index=int(detector[-1])-1

                        #Defining uncertainty band
                        edge_array=[]
                        percentage=detaljson["Alarm_Actions"]["edge_percentage (%)"]/100
                        for i in range(1,5):
                            edge=(float(attrs["Condition "+str(i)][1])-float(attrs["Condition "+str(i)][0]))*percentage
                            edge_array.append(edge)
                        
                        #Checking alarm levels interval triggering.
                        CheckAlarmCond(detector, attrs, detaljson, edge_array, trigger, detmonjson, 4)
             

                if stop():
                    print("Stopping Control Script.\n")
                    break

        else:
            print("No InMemDb. Quitting.")

    except Exception as e:
        print("Error in Control script: "+str(e))

    print("Finishing Control")
    
        

        
    
    
    


        
            
        

                
        
