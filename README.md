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
1. Write raspberry pi os LITE (32 bit) [release 2022-09-22] to an sd card (recommended 16 GB) with the following settings: 
   - hostname: pieye-[name].local. choose one of: (pieye-ant.local, pieye-beetle.local, pieye-cicada.local, pieye-dragonfly.local, pieye-earwig.local)
   - username: pi 
   - password: see NHMD secrets 
   - locale settings: Denmark
2. Once the pi OS has been installed on the sd card, enable the device to be run in usb device mode by completing the following:
    1. with the sd card still in your computer, edit the following in the 'boot' partition of the sd card (see the 'boot files' folder for some examples of what these should look like, but note that you cannot just copy these directly):
        1. config.txt - comment out the line `# otg_mode=1` and add the line `dtoverlay=dwc2` to the bottom of the file
        2. ssh - add an empty file called "ssh" to the boot partition - this enables ssh
        3. cmdline.txt - insert `modules-load=dwc2,g_ether g_ether.host_addr=00:22:82:ff:ff:20 g_ether.dev_addr=00:22:82:ff:ff:22` after rootwait. ensure there is one single space on either side of the command, and ensure the mac addresses are different for the different pis. - specifying the mac addresses is necessary because by default the mac address changes on reboot, and then the network settings are reset which is annoying. For each pi I changed the address by modifying the last letter in the mac address to match the pi - ie `00:22:82:ff:fa:20` and `00:22:82:ff:fa:22` for pieye-ant.local
3. Put the sd card into the zero, plug it into power and one cable to your computer. Your computer should now be able to connect via usb-ethernet to the raspberry pi zero. (try `ssh pi@pieye-ant.local`)
4. [Linux] Ensure in your network settings that ipv4 and ipv6 are set to 'shared to other computers' - this allows the pi to access the internet through your computer
4. [Mac] Ensure internet sharing is turned on - this allows the pi to access the internet through your computer
4. [Windows] Share your internet connection with the pi zero. This can be done by setting up a bridge connection between the pi zero and your internet connection.
5. [Linux] Once it says 'connected', you should be able to ssh into the pi - `ssh pi@pieye-ant.local` #(note, must be lowercase)
5. Check that the pi is able to access the internet - try `ping google.com` once you are remotely connected to the pi - if not, try restarting both the pi and the computer
6. Install git and pip
```bash
sudo apt-get update -y 
sudo apt-get install git -y
sudo apt-get install python3-pip -y
```
5. Clone git repo `git clone https://github.com/NHMDenmark/Pi-Eye.git`
6. Run setup.sh that installs some extras and sets up the pieye service `sudo chmod +x Pi-Eye/install_pieye.sh`, `./Pi-Eye/install_pieye.sh`

# Update Instructions
To update your Pi-Eye, use the provided script that automates the update process. Run the following command in your terminal:
```bash
sudo chmod +x Pi-Eye/scripts/update_pieye.sh
./Pi-Eye/scripts/update_pieye.sh
```

# Uninstall Instructions
To uninstall your Pi-Eye, use the provided script that automates the uninstall process. Run the following command in your terminal:
```bash
sudo chmod +x Pi-Eye/scripts/uninstall_pieye.sh
./Pi-Eye/scripts/uninstall_pieye.sh
```


# Physical Setup
The raspberry pi zeros are physically mounted onto the raspberry pi HQ cameras using the 3d printed mounts.


TODO
1. Make a service to update the git on the pi automatically if there is a new release - including copying the pieye.service file and rebooting the service? - if this works, remove the cronjob from setup.sh
2. Make requirements file so all python versions stay fixed . install from said file
3. Add photo of single pi-eye with arrows pointing to things


Troubleshootig Pieyes

1. ssh into Pieye: ssh pi@pieye-name.local
2. Check status of Pieye: sudo systemctl status pieye
3. Try restart with: sudo systemctl restart pieye
4. Try runnng script manually with `python3 -m pieye`or `pieye`
5. Try reboot with: sudo reboot
6. delete __pycache__ on pieye 
