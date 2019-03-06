# CaptivePortal
A captive portal with FreeIPA authentication used for TIHLDE LAN.

## Installation and setup (*WIP*)
### Note: These steps do not include setting up a TLS cert in nginx for HTTPS.
1. Set up bridging of network interfaces, using DHCP to aquire IP address
2. Install `nginx`, `python3` and python packages: `sudo pip3 install -r requirements.txt`
3. Adjust config in file `config.yml` and run `sudo python3 setup.py`
5. Install systemd service file found in `systemd/captiveportal.service`
6. Enable and start the `captiveportal` systemd service
7. Enable nginx site configs found in `nginx/sites-available`

## Note on the event of reboot
Iptables rules will be lost on reboot. To ensure database and iptables are in sync, run the `setup.py` script after the event of a reboot. **Be warned that this flushes and removes all client entries, meaning all users must re-authenticate.**
