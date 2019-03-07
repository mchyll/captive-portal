# TIHLDE LAN Captive Portal
A captive portal with FreeIPA authentication used at TIHLDE LAN parties.

The captive portal runs on a server which acts as a transparent firewall. A router with DHCP server and NAT is at the side of the server connected to the internet, while players at the LAN party is at the other side.

## Installation and setup
**Note**: These steps assume the application is installed into `/home/drift/CaptivePortal/`, and that we'll use the domain `lan.tihlde.org` for Loke (the server running the captive portal). This can be changed by changing the relevant paths and names in a few of the files.

1. Set up bridging of network interfaces, using DHCP to aquire IP address
2. Set DNS entry for `lan.tihlde.org` to local IP of Loke
3. Install `nginx`, `python3` and python packages: `sudo pip3 install -r requirements.txt`
4. Copy `config.yml.template` to `config.yml`, adjust the config params and run `sudo python3 setup.py`
5. Install systemd service file found in `systemd/captiveportal.service`
6. Enable and start the `captiveportal` systemd service
7. Insert paths of TLS certificate and private key issued for `lan.tihlde.org` in the `nginx/sites-available/lan.tihlde.org.conf` config
8. Enable the nginx sites found in `nginx/sites-available/` by symlinking the site configs into `/etc/nginx/sites-enabled/`, and reloading the nginx service

## Note on the event of reboot
Iptables rules will be lost on reboot. To ensure database and iptables are in sync, run the `setup.py` script after the event of a reboot. **Be warned that this flushes and removes all client entries, meaning all users must re-authenticate.**
