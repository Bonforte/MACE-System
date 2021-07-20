#!/bin/sh

influx -database 'CRIO' -host 172.18.4.156 -port 8086 -execute "show measurements"
