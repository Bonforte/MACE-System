#!/usr/bin/env python3

from flask import Flask, render_template, request,g,redirect,session,url_for
import os
from influxdb import InfluxDBClient

with open('/home/eliade/MAC-System-Grafana/GUI/Alarmconf.txt','r') as g1:
            values =g1.read().split(',')
            
headings=[]
data=[]
results=[]
client=InfluxDBClient(host='172.18.4.156',port='8086',database='AlarmDB')
result=client.query('select * from AlarmTable')

if result:
    headings=result.raw['series'][0]['columns']
    for entry in result.raw['series'][0]['values']:
        data.append(entry)


app=Flask(__name__)

#Creating login section:
class User:
    def __init__(self,id,username,password):
        self.id=id
        self.username=username
        self.password=password

users=[]
users.append(User(id=1,username='eliademace',password='Analiza_E8'))

app.secret_key='Analiza_E8'

@app.before_request
def before_request():
    g.user=None

    if 'user_id' in session:
        user=[x for x in users if x.id==session['user_id']][0]
        g.user=user

@app.route('/', methods=['GET','POST'])
def login():
    if request.method=='POST':
        session.pop('user_id',None)
        username=request.form['username']
        password=request.form['password']

        user=[x for x in users if x.username==username][0]
        if user and user.password==password:
            session['user_id']=user.id
            return redirect(url_for('index'))
        return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/ELIADE-MACE')

def index():
    if not g.user:
        return redirect(url_for(''))
    with open("/home/eliade/MAC-System-Grafana/GUI/wait_time.txt",'r') as g2:
        wtime=g2.read()
    return render_template('index.html',headings=headings, data=data,values=values,wtime=wtime)

@app.route('/ELIADE-MACE',methods=['GET'])
def index_get1():
    if not g.user:
        return redirect(url_for(''))
    if request.method=='GET':
        with open('/home/eliade/MAC-System-Grafana/GUI/Alarmconf.txt','r') as g1:
            values =g1.read().split(',')
    return render_template('index.html',headings=headings, data=data,values=values)

@app.route('/ELIADE-MACE',methods=['GET'])
def index_get2():
    if not g.user:
        return redirect(url_for(''))
    if request.method=='GET':
        with open('/home/eliade/MAC-System-Grafana/GUI/wait_time.txt','r') as g2:
            wtime =g2.read()
    return render_template('index.html',headings=headings, data=data,values=values,wtime=wtime)

@app.route('/ELIADE-MACE',methods=['POST'])
def index_post1():
    if not g.user:
        return redirect(url_for(''))
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
    app.run(host=os.getenv('IP','172.18.4.156'),port=int(os.getenv('PORT',24013)),debug=True)