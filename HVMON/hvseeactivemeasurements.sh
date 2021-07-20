#!/bin/sh

influx -database 'HVMonitor' -host 172.18.4.156 -port 8086 -execute "show measurements"
