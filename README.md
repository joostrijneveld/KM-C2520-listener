## Scanner daemon for the Kyocera Mita C2520

This is work in progress, and not yet usable at all.

This project is an attempt to provide a listener for the Kyocera Mita C2520 that runs on an Intel Mac platform. The original OSX listener as provided by Kyocera Mita (found [here](http://www.kyoceradocumentsolutions.eu/index/service/dlc.false.driver.KMC2520._.EN.html)) was only compiled for the PowerPC platform, and no longer works on OS X 10.7 and onwards.

Currently it only runs as a one-shot Python script that simulates network interaction according to the protocol that the scanner seems to understand. The PDFs it extracts from the received traffic are not yet flawless (but a clean-script is included), it is not yet robust against cancellation and interruptions and leaves the scanner is an erroneous state after execution.

The file `scannerscript.py` provides the listener, and `clean.py` cleans up the output file as provided by the listener. These should be merged.

One might say it is pre-alpha.

### TODO
* Combine listener and cleaner
* Properly close the interaction
* Provide robustness against input other than the happy path
* Run as a system daemon
* Adhere to specified file names as sent by the scanner

### Notes
Currently the PDF contains the following issues:

* Each block of 16x1460+1218 bytes is prefixed with a size indicator
* The file starts with two null bytes that need to be ignored

Both these issues are fixed by the clean.py file. Additionally, clean.py drops bytes that are written past the EOF, but this is no longer an issue with the current listener.