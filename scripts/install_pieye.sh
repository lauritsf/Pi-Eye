#!/bin/bash

REPO_URL="https://github.com/NHMDenmark/Pi-Eye.git"

# Clone repository
git clone "$REPO_URL" /home/pi/Pi-Eye

# Change directory
cd /home/pi/Pi-Eye

# Install the Python package
pip install .

# Copy the .service file to systemd directory
sudo cp pieye.service /lib/systemd/system/

# Enable and start the service
sudo systemctl enable pieye.service
sudo systemctl start pieye.service

# Turn on watchdog
sudo sed -i 's/#RuntimeWatchdogSec=0/RuntimeWatchdogSec=10/' /etc/systemd/system.conf
sudo sed -i 's/#ShutdownWatchdogSec=10min/ShutdownWatchdogSec=2min/' /etc/systemd/system.conf

# Get version of package
VERSION = $(python -c "import pieye; print(pieye.__version__)")

echo "Pi Eye Camera Service has been installed with version $VERSION."