#!/bin/sh

echo "Please enter the name of the table you want to delete"

read tablename1



influx -database 'CRIO' -host 172.18.4.156 -port 8086 -execute "drop measurement $tablename1"
