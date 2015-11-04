#PyGPS
PyGPS is a package of GPS tools for Python. It contains the following:

**[serialGPS](#serialgps)**  
**[NMEA](#nmea)**  
**[kmlIO](#kmlio)**  
**[Example Program](#example-program)**  
  
  
##serialGPS
Provides interface with any serial-connected GPS module. The serialGPS object reads from the GPS on a separate thread, so it is designed to be non-blocking.

**Requirement: [pyserial](https://github.com/pyserial/pyserial)**

####Usage: 
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
 
Finally, when done reading from the port, simply call:
```python
s.close()
```

##NMEA
Contains classes for dealing with NMEA sentences and other relevant data. Currently contains:
- **Point**
  - *lat*: Latitude (decimal value)
  - *lng*: Longitude (decimal value)
  - *alt*: Altitude in meters
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

##kmlIO
Provides methods for converting PyGPS data to Keyhole Markup Language (KML) files. Currently includes the following methods:

`pointsToKML(points, filename)`: Converts a list of points to a KML file.  
`pathToKML(path, filename)`: Converts a list of ordered points to a path in a KML file.

*[Learn more about KML here](https://developers.google.com/kml/)*

## Example program:
###recorder.py
Recorder is an example program which connects to a GPS module over serial, and records the incoming points until the user stops it. Usage is as follows:

```
$ python examples/recorder.py port [-outputKML <outputfile>]
```

If the optional argument ```-outputKML``` is not given, the points are simply output to the console when complete.

With an output KML files specified, running recorder might look something like this:
```
Attempting to open serial port: /dev/tty.usbserial-AH02F1FF
Serial Port open sucessfully! Waiting for satellite fix...
Satellite Fix! Recording points.
Press enter to stop recording: 
Recorded 104 points
```
Uploading the KML file to Google MyMaps can help visualize the points:
<img src="http://i.imgur.com/UkWLIyS.png"/>

To see how recorder.py works, just [take a look at the source](examples/recorder.py)
- - -
*Copywrite (c) 2015 Cody Smith, Apache License Version 2 (APLv2), see [LICENSE file](LICENSE)*
