# Pi-Eye
Prototype code for single pi-hq camera server for pinned insect digitization. Physical digitization station design based on ALICE (https://www.doi.org/10.17605/OSF.IO/UVWRN). Repository for related GUI: https://github.com/NHMDenmark/EntomoloGUI

# General Idea
There are five Pi-Eyes in total: four to take angled images of the labels, and one to take a top view of the qr code label before it is pinned. 

# Things you need
Each pi-eye has several components:
1. A raspberry pi zero 2W with power cable, micro usb cable and flexible ribbon for cameras
2. A raspberry pi HQ camera and lens (lens choice depends on requirements for the project)
3. A 16 GB sd card for the operating system to be installed on (you will probably need a usb adapter to install the OS on the sd card)
4. A mounting plate for the raspberry pi zero (the files for the 3d printed one I used can be found under '3d prints' folder)
5. 8 M2 bolts (around 10mm) and nuts 

# Installation Instructions
## Raspberry Pi / Device Setup
We need to install the raspberry pi OS lite on the card and configure it to be able to connect to the internet via usb-ethernet. This is done by enabling the pi to be run in usb device mode. This is done by editing the files on the sd card before booting the pi.
### Flashing the sd card
1. Write Raspberry Pi OS Lite (32 bit) [release 2022-09-22] using the Raspberry Pi Imager to an sd card (recommended 16 GB) with the following settings: 
   - hostname: pieye-[name].local. choose one of: (pieye-ant.local, pieye-beetle.local, pieye-cicada.local, pieye-dragonfly.local, pieye-earwig.local)
   - username: pi 
   - password: ****** [see NHMD secrets]
   - locale settings: Denmark
2. The `bootfs` partition should be mounted automatically. If not, mount it manually.
3. We now need to modify the `bootfs` files. This can be done automatically or manually.


### bootfs file modifications (Automatic)
We can use `scripts/setup_pi_preboot.sh` to automatically modify the files on the sd card. This script will: 
1. Enable ssh
2. Enable usb-ethernet
3. Enable usb device mode
4. Set the MAC address of the pi zero

Execute the script, passing the device name and mount point of the sd card as arguments.
```bash
./scripts/setup_pi_preboot.sh <device name> <mount point>
```
Example:    
```bash
./scripts/setup_pi_preboot.sh pieye-ant /Volumes/bootfs
```

### bootfs file modifications (Manual)
If you prefer to modify the files manually, you can perform the following in the root of the `bootfs` partition:
1. Enable ssh by creating an empty file called "ssh" in the root of the boot partition
2. Enable usb-ethernet by adding `dtoverlay=dwc2` to the bottom of the `config.txt` file
3. Change `otg_mode=1` to `# otg_mode=1` in the `config.txt` file
4. In `cmdline.txt` insert `modules-load=dwc2,g_ether g_ether.host_addr=00:22:82:ff:ff:20 g_ether.dev_addr=00:22:82:ff:ff:22` after rootwait.
    - Keep one single space on either side of the command, and ensure the mac addresses are different for the different pis. Refer to the table below for the mac addresses for each pi.

    | Device hostname  | host_addr        | dev_addr        |
    | ------- | ---------------- | --------------- |
    | **X**name    | 00:22:82:ff:f**X**:20| 00:22:82:ff:f**X**:22|
    | pieye-ant     | 00:22:82:ff:fa:20| 00:22:82:ff:fa:22|
    | pieye-beetle  | 00:22:82:ff:fb:20| 00:22:82:ff:fb:22|
    | pieye-cicada  | 00:22:82:ff:fc:20| 00:22:82:ff:fc:22|
    | pieye-dragonfly | 00:22:82:ff:fd:20| 00:22:82:ff:fd:22|
    | pieye-earwig  | 00:22:82:ff:fe:20| 00:22:82:ff:fe:22|
3. Unmount the sd card and insert it into the pi zero. Plug the pi zero into your computer using the micro usb cable.
4. Share your internet connection with the pi zero.
    - [Mac] In network settings, a new network interface should appear called 'RNDIS/Ethernet Gadget'. If it does not connect automatically, try setting the ip address manually to `192.168.0.1`
    - [Windows] If internet sharing does not work, try setting up a bridge connection between the pi zero and your internet connection.
5. The raspberry pi should now be accessible on pieye-[name].local through mDNS. Confirm that you can see the pi by pinging it in the terminal: `ping pieye-[name].local` (eg. `ping pieye-ant.local`)
6. ssh into the pi using `ssh pi@pieye-[name].local` (eg. `ssh pi@pieye-ant.local`). You will need the ssh password from earlier (see NHMD secrets).
7. You can confirm that the pi is connected to the internet by pinging a website: `ping google.com`
8. Install git and pip:
```bash
sudo apt-get update -y && sudo apt-get install git python3-pip -y
```
## Pi-Eye installation
Once the Raspberry Pi has is setup, connected to the internet and has git and pip installed, we can install the Pi-Eye software.
### Option 1: Install from source and start service
The following will run the setup script, cloning the Pi-Eye repository and enabling the service
```bash
curl -sSL https://raw.githubusercontent.com/NHMDenmark/Pi-Eye/main/scripts/setup_pieye.sh | bash
```

### Option 2: Pip install, but no service
Note that this requires manually starting the service after each reboot.
```bash
python -m pip install git+https://github.com/NHMDenmark/Pi-Eye.git
```

# Usage Instructions
The Pi-Eye service is started automatically on boot. To check the status of the service, run the following command in your terminal:
```bash
systemctl status pieye
```
If the service is not installed, you can run the pieye software with
```bash
python -m pieye
```

# Update Instructions
To update your Pi-Eye, use the provided script that automates the update process. Run the following command in your terminal:
```bash
./Pi-Eye/scripts/update_pieye.sh
```

# Uninstall Instructions
To uninstall your Pi-Eye, use the provided script that automates the uninstall process. Run the following command in your terminal:
```bash
./Pi-Eye/scripts/uninstall_pieye.sh
```


# Physical Setup
The raspberry pi zeros are physically mounted onto the raspberry pi HQ cameras using the 3d printed mounts.



# Troubleshootig Pieyes
## Pieye does not show up when I ping it
1. Check that the pi is connected to the computer via usb
2. Check that the pi shows up in network settings
    - It should appear as a RNDS/Ethernet Gadget interface
    - Check that the ip address is set to `192.168.0.1`
3. Connect to monitor via hdmi and check for errors.
    - Check that the IP, hostname and mac addresses displayed on the screen are correct
    - Check that the pi is able to ping the computer at `192.168.0.1`
    - Check that the Pieye service is running without errors
4. Try rebooting the pi and reconnecting it to the computer

## The Pieye server does not respond
1. Check that you can ping the pieye from the computer
2. Check that the Pieye service is running without errors
    - ssh into the pieye: `ssh pi@pieye-[name].local`
    - Check status of Pieye: `sudo systemctl status pieye`
    - Try restarting the service with `sudo systemctl restart pieye`
    - Alternatively: check the status of the service with `journalctl -u pieye`
3. Try rebooting the pi and reconnecting it to the computer

# TODO
1. Make a service to update the git on the pi automatically if there is a new release - including copying the pieye.service file and rebooting the service? - if this works, remove the cronjob from setup.sh - However, consider if this is a good idea, as it might be better to have a manual update process to avoid breaking things
2. Make requirements file so all python versions stay fixed . install from said file
3. Add photo of single pi-eye with arrows pointing to things