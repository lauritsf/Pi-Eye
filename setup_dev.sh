#!/bin/bash

# install software needed
sudo apt-get update
sudo apt-get install git
sudo apt-get install python3-pip
sudo apt-get install libatlas-base-dev
sudo apt install python3-opencv

# get latest code
eval "$(ssh-agent)"
ssh-add ~/.ssh/id_github
ssh -T git@github.com # test
git clone git@github.com:NHMDenmark/Pi-Eye.git /home/pi/Pi-Eye
git config --global user.email "rehunt@ualberta.ca"
git config --global user.name "Roberta"

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