#!/bin/bash
set -e

DEFAULT_REPO_URL="https://github.com/NHMDenmark/Pi-Eye.git"

REPO_URL=${1:-$DEFAULT_REPO_URL} # Allow passing in a custom repository URL as first argument
REPO_DIR="/home/pi/Pi-Eye"

# Ensure git and pip are installed
command -v git >/dev/null 2>&1 || { echo "git is not installed. Exiting."; exit 1; }
command -v pip >/dev/null 2>&1 || { echo "pip is not installed. Exiting."; exit 1; }

# Check if repository directory exists
if [ -d "$REPO_DIR" ]; then
    echo "Directory $REPO_DIR already exists. Exiting."
    exit 1
fi

# Clone repository
git clone "$REPO_URL" "$REPO_DIR"

# Change directory
cd "$REPO_DIR"

# Install the Python package
pip install .

# Copy the .service file to systemd directory
sudo cp pieye.service /lib/systemd/system/

# Enable and start the service
sudo systemctl enable pieye.service
sudo systemctl start pieye.service
sudo systemctl is-active pieye.service || { echo "Failed to start pieye.service. Exiting."; exit 1; }

# Turn on watchdog
sudo sed -i 's/#RuntimeWatchdogSec=0/RuntimeWatchdogSec=10/' /etc/systemd/system.conf
sudo sed -i 's/#ShutdownWatchdogSec=10min/ShutdownWatchdogSec=2min/' /etc/systemd/system.conf

# Setup autologin (cli)
sudo raspi-config nonint do_boot_behaviour B2

# Copy display_info.sh to /home/pi folder
cp scripts/display_info.sh /home/pi

# Make display_info.sh execute on login
echo "bash /home/pi/display_info.sh" >> /home/pi/.profile

# Get version of package
VERSION=$(python -c "import pieye; print(pieye.__version__)")

echo "Pi Eye Camera Service has been installed with version $VERSION."