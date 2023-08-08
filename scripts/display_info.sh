#!/bin/bash

cleanup() {
    # Cleanup function to run on exit
    echo -e "\nStopping the info display..."
    clear
    exit 0
}

trap cleanup SIGINT # Run cleanup function on Ctrl+C

while :; do

    # Get IP address
    IP=$(hostname -I | awk '{print $1}')

    # Get Hostname
    HOSTNAME=$(hostname)

    # Get MAC address
    MAC_ADDRESS=$(ip link show usb0 | awk '/ether/ {print $2}')

    # Ping the Mac/PC (grab only second line)
    PING_RESULT=$(ping -c 1 192.168.0.1 | sed -n 2p)

    # Get ARP cache
    ARP_CACHE=$(arp -a)

    # Get the status of pieye.service
    PIEYE_STATUS=$(systemctl status pieye.service)

    # Get length of longest line in PIEYE_STATUS
    MAX_LENGTH=$(echo "$PIEYE_STATUS" | awk '{ if (length > max) {max = length} } END { print max }')

    clear # Clear the screen after all the information is gathered
    echo "System information:"
    echo "IP address: $IP"
    echo "Hostname: $HOSTNAME"
    echo "MAC address: $MAC_ADDRESS"
    echo -e "\nConection information:"
    echo "Ping result: $PING_RESULT"
    echo -e "ARP cache: \n$ARP_CACHE"
    echo -e "\nPieye service status:"
    printf "%-${MAX_LENGTH}s\n" "-" | tr ' ' '-'
    echo -e "$PIEYE_STATUS"

    echo -e "\nPress Ctrl+C to exit this status screen."

    sleep 10
done