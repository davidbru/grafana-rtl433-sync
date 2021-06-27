#!/bin/bash

BASEDIR=/home/plex/Documents/Scripts/TemperatureFlat/
LOGFILE=${BASEDIR}log.json
LOGDURATION=120


# remove old logfiles if it exists and recreate a new empty one
[ -e $LOGFILE ] && rm -- $LOGFILE
touch $LOGFILE

# listen for X seconds for sensor data and save it into the logfile
rtl_433 -F json:${LOGFILE} -T $LOGDURATION

# create valid json - part 1: replace "\n" with ","
LOGJSON=$(paste -sd, $LOGFILE)

# create valid json - part 1: wrap with "[" & "]" and export back to $LOGFILE
echo "[${LOGJSON}]" > $LOGFILE

python3 ${BASEDIR}2_parse_temperature_log.py