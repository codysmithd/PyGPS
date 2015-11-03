# PyGPS
Python GPS tools. PyGPS contains the following:

###NMEA
Contains classes for NMEA sentences. Currently, supports:
- **GGA**
  - *time*: UTC time
  - *lat*: Latitude (decimal value)
  - *lng*: Longitude (decimal value)
  - *fix_quality* (integer)
  - *num_sats*: Number of satellites being tracked
  - *hdp*: Horizontal dilution of position
  - *alt*: Altitude, Meters, above mean sea level
  - *geoid_height*: Height of geoid (mean sea level) above WGS84 ellipsoid
  - *checkum*: message checksum

###serialGPS
Provides interface with any serial-connected GPS module. The serialGPS object reads from the GPS on a separate thread. It is designed to be used in the following way:

##### Requirement: [pyserial](https://github.com/pyserial/pyserial)

First, the serialGPS object is created with the path to the port where the GPS module is connected:
```python
s = serialGPS('/dev/tty-usbMYPORT')
```
Next, when ready to open the port and read from the GPS:
```python
s.open()
```
As messages come in from the GPS, serialGPS maintains the state of the module, and has the following attributes:
 - ```.sat_fix```, boolean indicating if the module has a satellite fix.
 - ```.data```, list of valid NMEA message objects recieved post satellite fix
 -
Finally, when done reading from the port, simply call:
```python
s.close()
```

###kmlIO
Provides methods for convering PyGPS Points to KML and KMZ files.

## Example program:
###recorder.py
Recorder is an example program which connects to a GPS module over serial, and records the incoming points until the user stops it. Usage is as follows:

```
$ python examples/logger.py -port <serialPort> (-outputKML <outputfile>)
```

If the optional argument ```-outputKML``` is not given, the points are simply output to the console when complete.
