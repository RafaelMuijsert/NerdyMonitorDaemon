#!/bin/bash

# Read configuration

while true
do
	# Measure each component
	source uptime.sh
	source cpu-load.sh
	source disk-space.sh
	# Sleep n seconds
	sleep 2
	
done
