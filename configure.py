#!/usr/bin/env python3
# Written by Dawid Kulikowski

import os
import sys
import uuid

PATH_CONF = "/etc/NetworkManager/system-connections/eduroam.nmconnection" 

nm_conn_conf = """
[connection]
id=eduroam
uuid=%s
type=wifi
interface-name=wlan0

[wifi]
mode=infrastructure
ssid=eduroam

[wifi-security]
auth-alg=open
key-mgmt=wpa-eap

[802-1x]
eap=peap;
identity=%s
password=%s
phase2-auth=mschapv2

[ipv4]
method=auto

[ipv6]
addr-gen-mode=stable-privacy
method=auto

[proxy]

"""

network_setup = [
    "rfkill unblock wifi", # Enable wifi
    "sed -i 's/^managed=.*$/managed=true/' /etc/NetworkManager/NetworkManager.conf", # Enable full authority over networking
    "systemctl disable --now dhcpcd", # Disable old networking
    "systemctl enable --now NetworkManager", # Enable NetworkManager
    "nmcli radio wifi on",
]

def write_nm_conn_conf(username: str, password: str):
    with open(PATH_CONF, "w") as f:
        f.write(nm_conn_conf % (uuid.uuid4(), username, password))

    os.chmod(PATH_CONF, 0o600) # Username/password combo is stored here and NM will complain if it's not secure

if __name__ == "__main__":
    if os.getuid() != 0: # Most of network setup requires superuser privilages, easiest to just run the whole script as root
        print("Please run this script as root!")
        sys.exit(1)

    email = input("What's your student email? ") # Emails are notoriously difficult to validate, so we'll just assume it's correct
    password = input("What's your student email password? ") # Can't validate password without internet, assume it's correct

    write_nm_conn_conf(email, password)

    country = input("What's your country code? (Search ISO 3166 alpha-2 if unsure) ") # Used to configure wifi channels + tx power

    cc_sed_cmd =  f"sed -i 's/^REGDOMAIN=.*$/REGDOMAIN={country}/' /etc/default/crda" # Set wifi country code
    os.system(cc_sed_cmd)

    for cmd in network_setup:
        os.system(cmd)

    print("All done! Reboot with `sudo reboot` for changes to fully take effect")


