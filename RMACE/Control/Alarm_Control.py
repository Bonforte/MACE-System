#!/usr/bin/env python3
import redis
import json
import time

with open("/home/eliade/Desktop/RMACE/Confjson/db_config_settings.json","r") as db_json:
    json_object=json.load(db_json)
    
host=json_object["Credentials"]["redis_ip"]
port=json_object["Credentials"]["redis_port"]
db=json_object["Credentials"]["redis_db_no"]

redb=redis.Redis(host,port,db)

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

                        #email
                        if Check_in_Limits(detmonjson["CurrentTemp"][index],attrs["Condition 1"][0],attrs["Condition 1"][1],edge_array[0]):
                            #Recording Trigger time:
                            
                            
                            #Trigger increments:
                            detaljson[str(detector)]['Triggers'][0]+=1

                            #If trigger value is reached:
                            if detaljson[str(detector)]['Triggers'][0]>=trigger:
                                #Alarm level is changed and triggers are reset for respective detector for efficiency:
                                detaljson[detector]['AlarmLevel']=1
                                for z in range(len(detaljson[str(detector)]['Triggers'])):
                                    # -1 of value??
                                    detaljson[str(detector)]['Triggers'][z]=0
                        #call
                        
                        elif Check_in_Limits(detmonjson["CurrentTemp"][index],attrs["Condition 2"][0],attrs["Condition 2"][1],edge_array[1]):
                            
                            #Trigger increments:
                            detaljson[str(detector)]['Triggers'][1]+=1

                            #If trigger value is reached:
                            if detaljson[str(detector)]['Triggers'][1]>=trigger:
                                #Alarm level is changed and triggers are reset for respective detector for efficiency:
                                detaljson[detector]['AlarmLevel']=2
                                for z in range(len(detaljson[str(detector)]['Triggers'])):
                                    detaljson[str(detector)]['Triggers'][z]=0
                        #sd
                        elif Check_in_Limits(detmonjson["CurrentTemp"][index],attrs["Condition 3"][0],attrs["Condition 3"][1],edge_array[2]):
                            
                            #Trigger increments:
                            detaljson[str(detector)]['Triggers'][2]+=1

                            #If trigger value is reached:
                            if detaljson[str(detector)]['Triggers'][2]>=trigger:
                                #Alarm level is changed and triggers are reset for respective detector for efficiency:
                                detaljson[detector]['AlarmLevel']=3
                                for z in range(len(detaljson[str(detector)]['Triggers'])):
                                    detaljson[str(detector)]['Triggers'][z]=0
                        #filling
                        elif Check_in_Limits(detmonjson["CurrentTemp"][index],attrs["Condition 4"][0],attrs["Condition 4"][1],edge_array[3]):
                            
                            #Trigger increments:
                            detaljson[str(detector)]['Triggers'][3]+=1

                            #If trigger value is reached:
                            if detaljson[str(detector)]['Triggers'][3]>=trigger:
                                #Alarm level is changed and triggers are reset for respective detector for efficiency:
                                detaljson[detector]['AlarmLevel']=4
                                for z in range(len(detaljson[str(detector)]['Triggers'])):
                                    detaljson[str(detector)]['Triggers'][z]=0
                        #no alarms
                        elif Check_out_Limits(detmonjson["CurrentTemp"][index],attrs["Condition 1"][0],attrs["Condition 4"][1]):
                            
                            #If trigger value is reached:
                            if detaljson[str(detector)]['Triggers'][4]>=trigger:
                                #Alarm level is changed and triggers are reset for respective detector for efficiency:
                                detaljson[detector]['AlarmLevel']=0
                                for z in range(len(detaljson[str(detector)]['Triggers'])):
                                    detaljson[str(detector)]['Triggers'][z]=0

                        #disconnected:
                        elif float(detmonjson["CurrentTemp"][index])>100:
                            detaljson[detector]['AlarmLevel']='dc'
                            for z in range(len(detaljson[str(detector)]['Triggers'])):
                                detaljson[str(detector)]['Triggers'][z]=0
                                
                        #edge
                        else:
                            
                            detaljson[str(detector)]['Triggers'][5]+=1
                            if detaljson[str(detector)]['Triggers'][5]>=trigger:
                                detaljson[detector]['AlarmLevel']='edge'
                
                redb.watch("Detectors_config")
                redjson=json.dumps(detcnfgjson,ensure_ascii=False).encode('utf-8')
                redb.set('Detectors_config',redjson)

                redb.watch("Detectors_Alarms")
                redjson=json.dumps(detaljson,ensure_ascii=False).encode('utf-8')
                redb.set('Detectors_Alarms',redjson)

                redb.watch("Monitoring_Data")
                redjson=json.dumps(detmonjson,ensure_ascii=False).encode('utf-8')
                redb.set('Monitoring_Data',redjson)

                if stop():
                    print("Stopping Control Script.\n")
                    break

        else:
            print("No InMemDb. Quitting.")

    except Exception as e:
        print("Error in Control script: "+str(e))

    print("Finishing Control")
    
        

        
    
    
    


        
            
        

                
        
