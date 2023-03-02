#!/bin/bash

# install software needed
sudo apt-get update -y
sudo apt-get install git -y
sudo apt-get install python3-pip -y
sudo apt-get install libatlas-base-dev -y
sudo apt install python3-opencv -y

# get latest code
git clone https://github.com/robertahunt/Pi-Eye.git /home/pi/Pi-Eye

sudo chmod +x Pi-Eye/setup.sh

# install python modules
python -m pip install bottle
python -m pip install matplotlib
python -m pip install -U numpy

# set up service to run API
sudo groupadd pieye
sudo usermod -G pieye pi
sudo usermod -a -G video pi # after opencv install, seems cannot access camera
sudo cp Pi-Eye/pieye.service /lib/systemd/system/
sudo systemctl enable pieye
sudo systemctl start pieye

# turn on watchdog
sudo sed -i 's/#RuntimeWatchdogSec=0/RuntimeWatchdogSec=10/' /etc/systemd/system.conf
sudo sed -i 's/#ShutdownWatchdogSec=10min/ShutdownWatchdogSec=2min/' /etc/systemd/system.conf

# turn on cronjob to update pieye git
sudo chmod +x Pi-Eye/cron_pull.sh
sudo echo "*/5 * * * * pi /bin/sh /home/pi/Pi-Eye/cron_pull.sh" > sudo /etc/cron.d/pieye_pull

