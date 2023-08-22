#!/bin/bash

cleanup() {
    # Cleanup function to run on exit
    echo -e "\nStopping the info display..."
    clear
    exit 0
}

trap cleanup SIGINT # Run cleanup function on Ctrl+C

get_dhcp_info() {
    # Extract dhcp information for usb0 interface
    DHCP_INFO=$(dhcpcd -4 -U usb0)

    IP_ADDRESS=$(echo "$DHCP_INFO" | awk -F"'" '/ip_address/ {print $2}')
    BROADCAST_ADDRESS=$(echo "$DHCP_INFO" | awk -F"'" '/broadcast_address/ {print $2}')
    DHCP_LEASE_TIME=$(echo "$DHCP_INFO" | awk -F"'" '/dhcp_lease_time/ {print $2}')
    DHCP_SERVER=$(echo "$DHCP_INFO" | awk -F"'" '/dhcp_server_identifier/ {print $2}')
    DOMAIN_SERVERS=$(echo "$DHCP_INFO" | awk -F"'" '/domain_name_servers/ {print $2}')

}

while :; do

    # Get IP address
    IP=$(hostname -I | awk '{print $1}')

    # Get Hostname
    HOSTNAME=$(hostname)

    # If IP address is empty, provide an informative message
    if [[ -z $IP ]]; then
        get_dhcp_info
        IP="IP address: $IP_ADDRESS"
        PING_RESULT="Ping cannot be performed without an IP."
        ARP_CACHE="ARP cache not available without an IP."
    else
        # Ping the Mac/PC (grab only second line)
        PING_RESULT=$(ping -c 1 192.168.2.1 | sed -n 2p)

        # Get ARP cache
        ARP_CACHE=$(arp -a)
    fi


    # Get MAC address
    MAC_ADDRESS=$(ip link show usb0 | awk '/ether/ {print $2}')

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
    if [[ -z $IP ]]; then
        echo "DHCP Information:"
        echo "Broadcast address: $BROADCAST_ADDRESS"
        echo "DHCP lease time: $DHCP_LEASE_TIME"
        echo "DHCP server: $DHCP_SERVER"
        echo "Domain name servers: $DOMAIN_SERVERS"
    fi
    echo -e "\nPieye service status:"
    printf "%-${MAX_LENGTH}s\n" "-" | tr ' ' '-'
    echo -e "$PIEYE_STATUS"

    echo -e "\nPress Ctrl+C to exit this status screen."

    sleep 10
done