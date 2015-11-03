'''
recorder.py
Example use of PyGPS to make a point recorder
Usage: $python3 logger.py -port <serialPort> (-outputKML <outputfile>)
'''

import os.path
import sys
sys.path.append('..')

from PyGPS.NMEA import Point
from PyGPS.NMEA import GGA
import PyGPS.serialGPS
from PyGPS.serialGPS import serialGPS
import time
from PyGPS.kmlIO import pointsToKml

# Parser for arguments
import argparse
parser = argparse.ArgumentParser(description="""Waits for serial-connected GPS to
get satellite fix and records points. After program is stopped,
optionally outputs those points to either command line or KML file.""")
parser.add_argument('-port', help='Path to port for serial connected GPS module (eg. /dev/tty-USB0)', required=True)
parser.add_argument('-v', help='verbose mode, print extra data')
parser.add_argument('-outputKML', help='(optional) filename for output KML')
args = parser.parse_args()

# Start program and input/output loop
print('Attempting to open serial port: ' + args.port)
s = serialGPS(args.port)
try:
    s.open()
    print('Serial Port open sucessfully! Waiting for satellite fix...')
    while not s.sat_fix:
        time.sleep(0.5)

    print('Satellite Fix! Recording points.')
    input('Press enter to stop recording: ')
    s.close()

    # Convert messages to points
    points = []
    for gga in s.data:
        points.append(Point(gga.lat, gga.lng, gga.alt))
    print( 'Recorded {0} points'.format(len(points)) )

    if args.outputKML != None:
        pointsToKml(points, args.outputKML)
    else:
        print('\nList of recorded points:')
        for point in points:
            print(point)

except PyGPS.serialGPS.SerialGPSOpenError:
    print('Error opening serial port, please check that the port path and name are correct.')
