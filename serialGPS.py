'''
serialGPS.py
Defines a serial-connected GPS module
Requires: pyserial (https://github.com/pyserial/pyserial)
'''

import NMEA
import serial

class serialGPS:
    '''
    serialGPS: Interface with a serial-connected GPS module
    Attributes:
        port: serial port to connect to (eg. '/dev/ttyUSB0')
        sat_fix: (bool) does the GPS have a satellite fix yet
        data: list of supported, valid NMEA objects received over the line (post sat_fix)
    '''
    def __init__(self, port=''):
        self.port = port
        self.data = []
        self.sat_fix = False

        self._ser = None

    # Opens the serial port
    def open(self):
        if self._ser != None:
            self._ser.close()
        self._ser = serial.Serial(self.port)

        line = self._ser.readline().decode().strip()
        while line:
            print(line)
            line = self._ser.readline().decode().strip()

    # Closes the serial port
    def close(self):
        self._ser.close()
        self._ser = None
