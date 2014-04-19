#! /bin/sh

echo 'Attempting to uninstall KM C25-20 scanner listener..'

launchctl unload ~/Library/LaunchAgents/nl.joostrijneveld.kmc2520.listener.plist
rm ~/Library/LaunchAgents/nl.joostrijneveld.kmc2520.listener.plist
sudo rm /usr/local/bin/kmc2520listener.py 
