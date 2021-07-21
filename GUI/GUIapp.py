#!/usr/bin/env python3

from flask import Flask, render_template, request
import os
from influxdb import InfluxDBClient

with open('/home/eliade/MAC-System-Grafana/GUI/Alarmconf.txt','r') as g1:
            values =g1.read().split(',')
            

results=[]
client=InfluxDBClient(host='172.18.4.156',port='8086',database='AlarmDB')
result=client.query('select * from alarms')

headings=result.raw['series'][0]['columns']
data=[]
for entry in result.raw['series'][0]['values']:
    data.append(entry)


app=Flask(__name__)



@app.route('/')
def index():
    with open("/home/eliade/MAC-System-Grafana/GUI/wait_time.txt",'r') as g2:
        wtime=g2.read()
    return render_template('index.html',headings=headings, data=data,values=values,wtime=wtime)

@app.route('/',methods=['GET'])
def index_get1():
    if request.method=='GET':
        with open('/home/eliade/MAC-System-Grafana/GUI/Alarmconf.txt','r') as g1:
            values =g1.read().split(',')
    return render_template('index.html',headings=headings, data=data,values=values)

@app.route('/',methods=['GET'])
def index_get2():
    if request.method=='GET':
        with open('/home/eliade/MAC-System-Grafana/GUI/wait_time.txt','r') as g2:
            wtime =g2.read()
    return render_template('index.html',headings=headings, data=data,values=values,wtime=wtime)

@app.route('/',methods=['POST'])
def index_post1():
    input_alarm=request.form['text_box']
    if request.method=='POST':
        with open('/home/eliade/MAC-System-Grafana/GUI/Alarmconf.txt','w') as f1:
            f1.write(str(input_alarm)+"\n")
        with open('/home/eliade/MAC-System-Grafana/GUI/Alarmconf.txt','r') as g1:
            values =g1.read().split(',')
    input_time=request.form['time_box']
    if request.method=='POST':
        with open('/home/eliade/MAC-System-Grafana/GUI/wait_time.txt','w') as f2:
            f2.write(str(input_time))
        with open('/home/eliade/MAC-System-Grafana/GUI/wait_time.txt','r') as g2:
            wtime=g2.read()
    return render_template('index.html',headings=headings, data=data,values=values,wtime=wtime)




if __name__=="__main__":
    #ip and port of running
    app.run(host=os.getenv('IP','172.18.4.156'),port=int(os.getenv('PORT',24013)),debug=True)