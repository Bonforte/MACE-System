#!/bin/sh

echo "Please enter the name of the table you want your data to be saved into. First for the detectors, then the valves:"

read tablename1
read tablename2


influx -database 'CRIO' -host 172.18.4.156 -port 8086 -execute "select * into CRIO..$tablename1 from CoolingSystemDet group by *"
influx -database 'CRIO' -host 172.18.4.156 -port 8086 -execute "select * into CRIO..$tablename2 from CoolingSystemValves group by *"
