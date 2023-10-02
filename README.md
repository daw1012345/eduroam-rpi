# Eduroam - RPi
## Description
A (very) basic script to connect the Raspberry Pi to Eduroam
## Purpose
It is not trivial to connect the Raspberry Pi to WPA2-Enterprise networks such as Eduroam. 
The GUI doesn't allow for it, and most of tutorials are convoluted and involve editing wpa-supplicant configuration files. 
This is not intuitive for e.g. university students with little experience working with Linux. This script simlifies the problem
to 3 pieces of information - the username, password and country code. This was originally made for the University of Twente (Operating Systems course - 2022 
edition).
## Use
1. Get the `configure.py` file onto the Raspberry Pi. This can be done with SCP, git, a USB drive, or the clipboard (copy-paste the contents)
2. (Optional) Inspect the script to ensure it doesn't do anything malicious. You're going to have to trust it with your username and password!
3. Execute it! Run `python3 configure.py`, with the working directory being the same as the containing folder of `configure.py`
4. Answer the questions when prompted. See this [list of country codes](https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes) if unsure what to answer for the last question. Use the Alpha-2 country code.

## Internals
This script replaces the network management system on the Pi with NetworkManager. It's much more intuitive and it makes the GUI applet more functional. It also configures the country code and enables wifi (if not already done). Then it generates and places a configuration file in the correct place using the username and password.
