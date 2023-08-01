#!/bin/bash

# Stop and disable the service
sudo systemctl stop pieye.service
sudo systemctl disable pieye.service

# Remove the service file from systemd directory
sudo rm /lib/systemd/system/pieye.service

# Uninstall the Python package
pip uninstall pieye

echo "Pi Eye Camera Service has been uninstalled."