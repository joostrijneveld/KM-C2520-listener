#! /bin/sh

cp kmc2520listener.py /usr/local/bin/
cp nl.joostrijneveld.kmc2520.listener.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/nl.joostrijneveld.kmc2520.listener.plist
echo 'Installed KM C25-20 scanner listener succesfully, started via launchd'
