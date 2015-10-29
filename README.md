# PyGPS
Python GPS tools.

##Modules:

###NMEA
Contains classes for NMEA sentences. Currently, only supports GGA.

###serialGPS
Provides interface with any serial-connected GPS module.
##### Requirements:
- [pyserial](https://github.com/pyserial/pyserial)

###kmlIO
Provides methods for convering PyGPS NMEA and Points to KML and KMZ files.
