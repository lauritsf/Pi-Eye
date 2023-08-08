#!/bin/bash
set -e

REPO_DIR="/home/pi/Pi-Eye"

# Ensure directory exists
if [ ! -d "$REPO_DIR" ]; then
    echo "Directory $REPO_DIR does not exist. Exiting."
    exit 1
fi

# Stop the service
sudo systemctl stop pieye.service

# Go to the repository
cd "$REPO_DIR"

# Check for local changes
if [ -n "$(git status -s)" ]; then
    echo "Local changes found. Exiting."
    exit 1
fi

# Get current version of package
OLD_VERSION=$(python -c "import pieye; print(pieye.__version__)")

# Update the repository
git pull

# Reinstall the Python package and its dependencies
pip install . --upgrade

# replace the .service file in systemd directory
sudo cp pieye.service /lib/systemd/system/

# Reload the service
sudo systemctl daemon-reload

# Start the service
sudo systemctl start pieye.service
sudo systemctl is-active pieye.service || { echo "Failed to start pieye.service. Exiting."; exit 1; }

# Get new version of package
NEW_VERSION=$(python -c "import pieye; print(pieye.__version__)")

echo "Pi Eye Camera Service has been update from version $OLD_VERSION to $NEW_VERSION."