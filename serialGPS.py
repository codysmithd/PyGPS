'''
serialGPS.py
Defines a serial-connected GPS module
Requires: pyserial (https://github.com/pyserial/pyserial)
'''

from PyGPS.NMEA import *
import serial
import threading
from threading import Thread

class serialGPS:
    '''
    Interface with a serial-connected GPS module

    Attributes:
        port: serial port to connect to (eg. '/dev/ttyUSB0')
        sat_fix: (bool) does the GPS have a satellite fix yet?
        data: list of supported, valid NMEA objects received over the line (post sat_fix).
        Utilized when port is opened without an 'on_data_fn' to act as a message buffer.

        _ser: (private) pyserial port
        _dataThread: (private) serialDataThread
    '''

    def __init__(self, port=''):
        self.port = port
        self.data = []
        self.sat_fix = False

        self._ser = None
        self._dataThread = None

    def open(self, on_data_fn):
        '''
        Attempts to open the port (self.port) with asynchronous serialDataThread
        and starts to store data after fix. If on_data_fn is utilized, serialGPS
        will NOT add to data.

        Args:
            on_data_fn: (optional) Function to run when a valid message is
            received. Function gets the received message as an NMEA object
        '''
        try:
            if self._ser != None:
                self._ser.close()
            self._ser = serial.Serial(self.port)

            if self._dataThread != None:
                self.dataThread.stop()
            self._dataThread = serialDataThread(self)
            self._dataThread.start(on_data_fn)
        except serial.serialutil.SerialException:
            if self._ser != None:
                self._ser.close()
            self._ser = None
            if self._dataThread != None:
                self.dataThread.stop()
            self._dataThread = None
            raise SerialGPSOpenError()

    def readData(self):
        '''
        Reads and clears buffered messages from the GPS.
        '''
        data = list(self.data)
        self.data = []
        return data

    def close(self):
        '''
        Stops reading from the serial connection, closes the serial port
        '''
        if self._dataThread:
            self._dataThread.stop()
            self._dataThread = None
        if self._ser:
            self._ser.close()
            self._ser = None

class serialDataThread(Thread):
    '''
    serialDataThread: Non-blocking (asynchronous) thread designed to read the
    serial data from the GPS unit. Either calls on_data_fn when valid data is
    received or adds it the serialGPS.data buffer.

    Attributes:
        sGPS: serialGPS object we are modifying
        _stop: (private) event to stop the thread
    '''
    def __init__(self, sGPS):
        Thread.__init__(self)
        self.sGPS = sGPS
        self._stop = threading.Event()

    # Run: reads lines from the GPS and processes and adds messages
    def run(self, on_data_fn):
        self._stop.clear()
        line = self.sGPS._ser.readline().decode().strip()
        while not self._stop.isSet() and len(line) > 0 and self.sGPS._ser != None:
            x = getNMEA(line)
            if type(x) is GGA:
                self.sGPS.sat_fix = (x.fix_quality != 0)
                if self.sGPS.sat_fix:
                    if on_data_fn:
                        on_data_fn(x);
                    else:
                        self.sGPS.data.append(x)
            try:
                line = self.sGPS._ser.readline().decode().strip()
            except TypeError:
                line = ''

    def stop(self):
        self._stop.set()

class SerialGPSOpenError(IOError):
    '''
    Error for when serial port cannot be opened
    '''
