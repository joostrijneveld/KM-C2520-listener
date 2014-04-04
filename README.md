## Scanner daemon for the Kyocera Mita 2530

This is work in progress, and not yet usable at all.

This project is an attempt to provide a listener for the Kyocera Mita 2530 that runs on an Intel Mac platform. The original OSX listener as provided by Kyocera Mita (found [here](http://www.kyoceradocumentsolutions.eu/index/service/dlc.false.driver.KM2530._.EN.html)) was only compiled for the PowerPC platform, and no longer works on OS X 10.7 and onwards.

Currently it only runs as a one-shot Python script that simulates network interaction according to the protocol that the scanner seems to understand. The PDFs it extracts from the received traffic are not yet flawless, it is not yet robust against cancellation and interruptions and leaves the scanner is an erroneous state after execution.

The file `scannerscript.py` provides the listener, and `clean.py` provides an initial attempt to clean up an output file as provided by the listener. These should be merged.

One might say it is pre-alpha.

### TODO
* Provide a correctly formatted PDF
* Properly close the interaction
* Provide robustness against input other than the happy path
* Run as a system daemon

### Notes
Currently the PDF contains the following issues:

* 0x6000 is added after each 16x1460+1218 set of bytes
* The file starts with an 0x0000 and an 0x6000
* Other differences exist

### Clean.py
* Removes 0x6000 added by the block separation
* Removes initial two bytes (as they are 0x0000 and 0x6000)
* Ends file at EOF (but should no longer be necessary)