#!/bin/bash
set -e

# Stop and disable the service
sudo systemctl stop pieye.service
sudo systemctl disable pieye.service
sudo systemctl daemon-reload

# Remove the service file from systemd directory
sudo rm /lib/systemd/system/pieye.service

# Uninstall the Python package
pip uninstall -y pieye

# Remove display_info.sh from /home/pi folder
rm /home/pi/display_info.sh

# Remove the line that executes display_info.sh on login
sed -i '/display_info.sh/d' /home/pi/.profile

# Remove cloned repository
rm -rf /home/pi/Pi-Eye

echo "Pi Eye Camera Service has been uninstalled."