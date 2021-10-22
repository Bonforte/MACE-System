#!/usr/bin/env python3
from os.path import dirname, join, abspath
import sys
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
import Alarm.Alarm_Funcs as af
import redis
import json
import time

#opening configuration file:
with open("/home/eliade/Desktop/RMACE/Confjson/db_config_settings.json","r") as db_conf:
    json_data=json.load(db_conf)

#Defining connection to redis:
redis_host=json_data["Credentials"]["redis_ip"]
redis_port=json_data["Credentials"]["redis_port"]
redis_db=json_data["Credentials"]["redis_db_no"]

redb=redis.Redis(redis_host,redis_port,redis_db)

def AlarmMonitoring(stop):
    inMemDb=redb.exists('Detectors_Alarms')
    
    if(inMemDb):
        while(True):
            time.sleep(1)

            #Loading redis into json
            datadetcnfg=json.loads(redb.get('Detectors_config').decode("utf-8"))
            datavar=json.loads(redb.get('Variables').decode("utf-8"))
            datadetal=json.loads(redb.get("Detectors_Alarms").decode("utf-8")) 
            
            #Initializing working arrays:
            alarmlvllist=[]
            detlist=[]      

            #Recording list of detectors that were activated for monitoring:
            for detector,attrs in datadetcnfg.items():
                if attrs['MonVar']:
                    detlist.append(str(detector))
            
            #Loading list of alarm levels from data structure:
            for i in datavar["alarmlvllist"]:
                alarmlvllist.append(i)

            #Iterating through alarms to see if something changed:
            for detector,attrs in datadetal.items():
                if detector[0:3]=="Det":
                    y=attrs['AlarmLevel']
                    if y==0:
                        datavar["alarmlvllist"][int(detector[-1])-1]=y

                    if (detector in detlist) and y and alarmlvllist[int(detector[-1])-1]!=y and y!='edge':

                        if y==1:
                            al_vec=datadetal["Alarm_Actions"]['1']['functions']
                            if al_vec:
                                for func in al_vec:
                                    exec("af."+func+"(detector[-1])")
                                al_vec=[]


                        elif y==2:
                            al_vec=datadetal["Alarm_Actions"]['2']['functions']
                            if alarmlvllist[int(detector[-1])-1]<y:
                                if al_vec:
                                    for func in al_vec:
                                        exec("af."+func+"(detector[-1])")
                                    al_vec=[]

                        elif y==3:
                            al_vec=datadetal["Alarm_Actions"]['3']['functions']
                            if alarmlvllist[int(detector[-1])-1]<y:
                                if al_vec:
                                    for func in al_vec:
                                        exec("af."+func+"(detector[-1])")
                                    al_vec=[]

                        elif y==4:
                            al_vec=datadetal["Alarm_Actions"]['4']['functions']
                            if alarmlvllist[int(detector[-1])-1]<y:
                                if al_vec:
                                    for func in al_vec:
                                        exec("af."+func+"(detector[-1])")
                                    al_vec=[]

                        datavar["alarmlvllist"][int(detector[-1])-1]=y
                        
            
            #Load data to redis
            redb.watch('Variables')
            redjson=json.dumps(datavar,ensure_ascii=False).encode('utf-8')
            redb.set('Variables',redjson)

            redb.watch('Detectors_Alarms')
            redjson=json.dumps(datadetal,ensure_ascii=False).encode('utf-8')
            redb.set('Detectors_Alarms',redjson)

            redb.watch('Detectors_config')
            redjson=json.dumps(datadetcnfg,ensure_ascii=False).encode('utf-8')
            redb.set('Detectors_config',redjson)

            #if data['Variables']['stopvar']==1:
                #stop=1
                
            if stop():
                
                print("Stopping Alarm Handler.")
                break
    else:
        print("No InMemDB.")

    
    print("Finishing Alarm Handler.")


    

    
        
        


