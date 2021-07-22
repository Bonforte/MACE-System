####################################
#README Updated Version: 22.08.2021#
#################################### 

Welcome to the MACE (Monitor, Alarm, Control for ELIADE) instructions:

############################################################################################

Grafana Monitoring: 172.18.4.156:3010
Website GUI for settings: 172.18.4.156:24013

############################################################################################

Before each PC-Server restart make sure influxdb and grafana-server services are running.

sudo systemctl restart influxd
sudo systemctl restart grafana-server

Also run this command for the SIMCall script:

sudo adb start-server

############################################################################################

Description of scripts:

GUI Folder:
-GUIapp.py- starts the webpage which runs on 172.18.4.156:24013 and runs on the internal network.
You can configure the alarm limits here for MACE.
-Alarmconf.txt- text file that contains the alarm limits for the system to use.
-wait_time.txt- text file that contains the time between read-outs for HV monitoring.
-Other files were used for the construction of the website.

HVMON Folder:
-HVConfiguration.xml- Contains the structure of the inserted boards and their respective number of channels for the CAEN SY4527 HV Source.
-hvinto_xml.py- Script used to modify the previous XML file, if the structure of the inserted boards was changed.
-HVMonInflux.py- Script that begins the monitoring of HV and leakeage current.
-The other files are bash scripts to manage the InfluxDB databases and recorded measurements.

CRIO Folder:
-CRIO.py- Script that begins the monitoring of the detector and valve temperature.
-The other files are bash scripts to manage the InfluxDB databases and recorded measurements.

Control Folder:
-Control.py- Script that begins directly monitoring the values of temperature and initiates trigger filling and shut down commands, in case of alarm trigger.
-ch_to_det_map.xml- XML file that maps the detectors to their specific slot and channels of the HV CAEN SY4527 power source.
-ctrlinto_xml.py- Script used to modify the previous XML file, if the detectors are being connected to different channels.

Alarm Folder:
-SIMCall.py- Script that begins directly monitoring the values of temperature and initiates a sim call if no internet connection is detected, in case of alarm trigger.
-TwCall.py- Script that begins directly monitoring the values of temperature and initiates an internet call, using Twilio, if there is internet connection, in case of alarm trigger.

############################################################################################

InfluxDB databases description:
-CRIO- database that records the measurements from CRIO.py, retention policy 21 days.
-HVMonitor- database that records the measurements from HVMonInflux.py, retention policy 21 days.
-AlarmDB- database that records previous triggered alarms, retention policy 42 days.

Access InfluxDB shell for executing InfluxQL commands:

influx -host yourip -port yourport

If you are on the original server yourip is 172.18.4.156 and yourport is 8086.

example: influx -host 172.18.4.156 -port 8086

Some basic InfluxQL commands:
-show databases
-use databasename(where databasename is the name of the database you desire to use)
-show measurements(once you are in the desired database it will show you the measurements (they are called tables in conventional database languages) in it)
-select * from measurementname (where measurementname is the name of the measurement you desire to see)
-delete from measurementname (deletes desired measurement)
-exit (exits InfluxShell)

###########################################################################################

For questions contact: George Nitescu, Technician, george.nitescu@eli-np.ro
