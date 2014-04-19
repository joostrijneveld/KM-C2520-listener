#! /bin/sh

launchctl unload ~/Library/LaunchAgents/nl.joostrijneveld.kmc2520.listener.plist
rm ~/Library/LaunchAgents/nl.joostrijneveld.kmc2520.listener.plist
rm /usr/local/bin/kmc2520listener.py 
echo 'Uninstalled KM C25-20 scanner listener succesfully'
