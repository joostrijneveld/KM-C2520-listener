## Scanner daemon for the Kyocera Mita C2520

This is work in progress, and might prove to be unstable. However, after several months of testing in a deployment situation, it has not caused any errors and has proven to be sufficiently robust.

Current version: 1.0.1

This project is an attempt to provide a listener for the Kyocera Mita C2520 that runs on an Intel Mac platform. The original OSX listener as provided by Kyocera Mita (found [here](http://www.kyoceradocumentsolutions.eu/index/service/dlc.false.driver.KMC2520._.EN.html)) was only compiled for the PowerPC platform, and no longer works on OS X 10.7 and onwards.

Currently it can be directly executed or run via launchctl on the background. This last way is preferred, as this ensures that the script is started when OSX starts. The script is still a bit rough around the edges, and might lead to unexpected errors. If this is the case, it does close cleanly and continues listening for a new attempt.

### Installation

To obtain the required files, either clone this repository or download the [latest release](https://github.com/joostrijneveld/KM-C2520-listener/releases).

Simply run `INSTALL.sh` from the command-line (i.e. navigate to the folder and type `./INSTALL.sh`). This installation script places the Python script in `/usr/local/bin`, adds the configuration file to the user's launchd library and loads the configuration file.

To undo the above, run `UNINSTALL.sh`.
