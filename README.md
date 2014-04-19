## Scanner daemon for the Kyocera Mita C2520

This is work in progress, and might prove to be unstable.

Current version: 1.0.0

This project is an attempt to provide a listener for the Kyocera Mita C2520 that runs on an Intel Mac platform. The original OSX listener as provided by Kyocera Mita (found [here](http://www.kyoceradocumentsolutions.eu/index/service/dlc.false.driver.KMC2520._.EN.html)) was only compiled for the PowerPC platform, and no longer works on OS X 10.7 and onwards.

Currently it can be directly executed or run via launchctl on the background. This last way is preferred, as this ensures that the script is started when OSX starts. The script is still very rough around the edges, and might lead to unexpected errors. In this case, it does close somewhat cleanly and continues listening for a new attempt.

### Installation

To obtain the required files, either clone this repository or download the [latest release](https://github.com/joostrijneveld/KM-C2520-listener/releases).

Simply run `INSTALL.sh` from the command-line. This script places the Python script in `/usr/local/bin`, adds the configuration file to the user's launchd library and loads the configuration file.

To undo the above, run `UNINSTALL.sh`.
