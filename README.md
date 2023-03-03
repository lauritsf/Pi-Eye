# Pi-Eye
Prototype code for single pi-hq camera server for pinned insect digitization. Physical digitization station design based on ALICE (https://www.doi.org/10.17605/OSF.IO/UVWRN). Repository for full digitization station: https://github.com/robertahunt/Pi-Eyed-Piper


# Pi-Eyed-Piper
Prototype code for pinned insect digitization station at Natural History Museum of Denmark. General setup somewhat based on ALICE (https://www.doi.org/10.17605/OSF.IO/UVWRN)


# Steps for setup
1. Write raspberry pi os LITE (32 bit) to sd card - release 2022-09-22, with settings hostname: (pieye-ant.local, pieye-beetle.local, pieye-cicada.local, pieye-dragonfly.local, pieye-earwig.local), ssh key, username (pi) and password and locale settings
2. Enable device to be run in usb device mode:
    1. with the sd card still in your computer, edit the following in the 'boot' partition of the sd card, or copy the files from the 'boot files' folder to the boot partition
        1. config.txt - comment out the line `# otg_mode=1` and add `dtoverlay=dwc2` to the bottom of the file
        2. ssh - add an empty file called "ssh" to the boot partition
        3. cmdline.txt - insert `modules-load=dwc2,g_ether g_ether.host_addr=00:22:82:ff:ff:20 g_ether.dev_addr=00:22:82:ff:ff:22` after rootwait. ensure there is one single space on either side of the command, and ensure the mac addresses are different for the different pis. - specifying the mac addresses because by default the mac address changes on reboot, and then the network settings are reset which is annoying
3. Put the sd card into the zero, plug it into power and one cable to your computer. Your computer should now be able to connect via usb-ethernet to the raspberry pi zero. (try `ssh pi@pieye-ant.local`)
4. Ensure in your network settings that ipv4 and ipv6 are set to 'shared to other computers'
5. Once it says connected, you should be able to ssh into the pi - 
   `ssh pi@pieyene.local` #(note, must be lowercase)
5. Check that the pi is able to access the internet - `ping google.com` - if not, try restarting both the pi and the computer
6. Install git and pip
```bash
sudo apt-get update -y 
sudo apt-get install git -y
sudo apt-get install python3-pip -y
sudo apt-get install libatlas-base-dev -y # used for update numpy 
sudo apt-get install python3-opencv -y
```
5. Clone git repo 
     `git clone https://github.com/NHMDenmark/Pi-Eye.git`
   if in development - `scp /home/rob/.ssh/id_github pi@pieyene.local:/home/pi/.ssh/id_github` from main computer, then on pi - 
```bash
eval "$(ssh-agent)"
ssh-add ~/.ssh/id_github
ssh -T git@github.com # test
git clone git@github.com:NHMDenmark/Pi-Eye.git
git config --global user.email "rehunt@ualberta.ca"
git config --global user.name "Roberta"
```
6. Run setup.sh `sudo chmod +x Pi-Eye/setup.sh`, `./Pi-Eye/setup.sh`
6. Install bottle - 
```bashCONF_SWAPSIZE=2048
python -m pip install bottle
python -m pip install matplotlib
python -m pip install -U numpy
```
7. Make a new group for the pieye service - sudo groupadd pieye && sudo usermod -G pieye pi
```bash
sudo groupadd pieye
sudo usermod -G pieye pi
sudo usermod -a -G video pi # after opencv install, seems cannot access camera
```
5. Set up the pieye service 
```bash
sudo cp Pi-Eye/pieye.service /lib/systemd/system/
sudo systemctl enable pieye
sudo systemctl start pieye
```
6. optional - for development it was nice to run vscode remote to code on the pi, however, it kept restarting due to not enough memory/swap
   so installed sudo apt install zram-tools (see https://www.reddit.com/r/raspberry_pi/comments/wyi6yi/raspberry_pi_zero_2_suddenly_very_slow/)
   or increase swap size: `sudo nano /etc/dphys-swapfile` change `CONF_SWAPSIZE=100` to `CONF_SWAPSIZE=2048`. reboot after this
7. Enable the watchdog - `sudo nano /etc/systemd/system.conf` set these lines: RuntimeWatchdogSec=10, ShutdownWatchdogSec=2min - ensures the pi zero reboots if it starts using too much memory


TODO
1. Make a service to update the git on the pi automatically - including copying the pieye.service file and rebooting the service?
2. Make our own images for each pi? can easily be flashed onto the devices?
3. Make a service that deletes older images from /tmp folder when the folder gets too large
4. Make requirements file so all python versions stay fixed . install from said file
5. Add tests


