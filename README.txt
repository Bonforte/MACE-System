##################
OUTDATED
###############

Welcome to the MAC (Monitor, Alarm, Control) instructions:

Before each server restart make sure influxdb and grafana-server services are running.

sudo systemctl restart influxd
sudo systemctl restart grafana-server

To start HVMonitoring run HVMonInflux.py in HVMON directory
To start CRIO run CRIO.py in CRIO directory.

Walkthrough configuration files in HVMON directory:

--HVConfiguration.conf;

Write the active slots with their respective number of channels in this order:

ex: sl1,noch1,sl2,noch2,sl3,noch3

For example if we have a board active on slot 4 with 8 channels and one active on slot 7 with 12 channels we will write:

4,8,7,12

in the HVConfiguration.conf file

This process will be more easy when the AC part of MAC will be up and running.

--wait_time.conf

Here you will write a single number that represents the number of seconds between read-outs regarding the HV monitoring system.

Disclaimer: CRIO doesn't need any configuration files.


For questions contact: George Nitescu, Technician.
