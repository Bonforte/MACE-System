#!/bin/sh

echo Please enter the name of the table you want your data to be saved into:

read tablename

influx -database 'HVMonitor' -host 172.18.4.156 -port 8086 -execute "select * into HVMonitor..$tablename from HVMONDB group by *"
