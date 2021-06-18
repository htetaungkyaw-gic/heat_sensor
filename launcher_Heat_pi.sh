#!/bin/sh
# launcher_Heat_pi.sh

if ! pgrep -f Heat_sensor_pi.py
then
	cd /home/pi/Documents/Heat_sensor
        echo "$(date) Let's run again.from_p3b_to_aws" >> ./logs/cronlog_pi
        echo 1233 | sudo -S python3 Heat_sensor_pi.py >> ./logs/cronlog_pi

fi
