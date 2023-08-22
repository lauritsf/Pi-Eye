#!/bin/bash

# Raspberry Pi Setup Script
# This script automates the setup process for Raspberry Pi devices after flashing the SD card.
# It modifies the config.txt and cmdline.txt files and enables SSH for remote access.
# Usage: ./setup_raspberry_pi.sh <device_name> <path_to_boot_partition>
# Example: ./setup_raspberry_pi.sh pieye-ant /Volumes/bootfs


# Function to modify config.txt
modify_config_txt() {
  if [ -f "$1"/config.txt ]; then
    sed -i '' 's/^otg_mode=1/# otg_mode=1/' "$1"/config.txt
    echo "dtoverlay=dwc2" >> "$1"/config.txt
  else
    echo "config.txt not found in $1. Skipping modification."
    exit 1
  fi
}

# Function to add ssh file to boot partition
enable_ssh() {
  touch "$1"/ssh
}

# Function to modify cmdline.txt
modify_cmdline_txt() {
  device_name=$1
  host_addr=$(grep "$device_name" lookup_table.txt | awk '{print $2}')
  dev_addr=$(grep "$device_name" lookup_table.txt | awk '{print $3}')

  commands="modules-load=dwc2,g_ether g_ether.host_addr=${host_addr} g_ether.dev_addr=${dev_addr}"


  if [ -f "$2"/cmdline.txt ]; then
    # insert commands after rootwait
    sed -i '' "s/rootwait/rootwait ${commands}/" "$2"/cmdline.txt
  else
    echo "cmdline.txt not found in $2. Skipping modification."
    exit 1
  fi
}



# Main script
if [ $# -ne 2 ]; then
  echo "Usage: $0 <device_name> <path_to_boot_partition>"
  exit 1
fi

# Lookup table for MAC addresses
# Format: device_name host_addr dev_addr
cat <<EOF > lookup_table.txt
pieye-ant 00:22:82:ff:fa:20 00:22:82:ff:fa:22
pieye-beetle 00:22:82:ff:fb:20 00:22:82:ff:fb:22
pieye-cicada 00:22:82:ff:fc:20 00:22:82:ff:fc:22
pieye-dragonfly 00:22:82:ff:fd:20 00:22:82:ff:fd:22
pieye-earwig 00:22:82:ff:fe:20 00:22:82:ff:fe:22
EOF

# Validate the device name
device_name=$1
if ! grep -q "$device_name" lookup_table.txt; then
  echo "Invalid device name."
  exit 1
fi

# Check if config.txt exists and modify if present
if [ -d "$2" ]; then
  backup_config=$(mktemp "$2"/config.txt.bak.XXXXXXXXXX)
  cp "$2"/config.txt "$backup_config"
  modify_config_txt "$2"
else
  echo "Boot partition directory $2 not found."
  exit 1
fi

# Enable ssh
enable_ssh "$2"

# Modify cmdline.txt for the specified device
if [ -f "$2"/cmdline.txt ]; then
  backup_cmdline=$(mktemp "$2"/cmdline.txt.bak.XXXXXXXXXX)
  cp "$2"/cmdline.txt "$backup_cmdline"
  modify_cmdline_txt "$1" "$2"
else
  echo "cmdline.txt not found in $2. Skipping modification."
  exit 1
fi

# Success! Removing backup files since all modifications were successful.
rm -f "$backup_config" "$backup_cmdline"