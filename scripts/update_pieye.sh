#!/bin/bash

# Stop the service
sudo systemctl stop pieye.service

# Go to the repository
cd /home/pi/Pi-Eye

# Get current version of package
OLD_VERSION=$(python -c "import pieye; print(pieye.__version__)")

# Update the repository
git pull

# Reinstall the Python package
pip install . --upgrade

# replace the .service file in systemd directory
sudo cp pieye.service /lib/systemd/system/

# Reload the service
sudo systemctl daemon-reload

# Start the service
sudo systemctl start pieye.service

# Get new version of package
NEW_VERSION=$(python -c "import pieye; print(pieye.__version__)")

echo "Pi Eye Camera Service has been update from version $OLD_VERSION to $NEW_VERSION."