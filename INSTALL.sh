#! /bin/sh

echo 'Attempting to install KM C25-20 scanner listener, starting via launchd..'

if [ ! -d /usr/local/bin ]; then
	sudo mkdir -p /usr/local/bin
fi
sudo cp kmc2520listener.py /usr/local/bin/
cp nl.joostrijneveld.kmc2520.listener.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/nl.joostrijneveld.kmc2520.listener.plist
