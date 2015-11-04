'''
NMEA.py
Defines NMEA sentence and other useful classes
'''

class Point:
    '''
    Point: Simple coordinate point
    Attributes:
        lat: Latutude (decimal)
        lng: Longitude (decimal)
        alt: Altitude (meters)
    '''

    def __init__(self, lat=0, lng=0, alt=0):
        self.lat = lat
        self.lng = lng
        self.alt = alt

    def __str__(self):
        return '{0}, {1}, {2} meters'.format(self.lat, self.lng, self.alt)

    def getDistance(self, toPoint):
        '''
        Gets the distance (in arbitrary units) to another point
        '''
        return math.sqrt(math.pow((self.lat - toPoint.lat),2) + math.pow((self.lng - toPoint.lng),2))

class GGA :
    '''
    NMEA GGA: fix data
    Attributes:
        time: String with UTC time
        lat: Latitude (decimal value)
        lng: Longitude (decimal value)
        fix_quality:
            0 = Error (no fix)
            1 = GPS fix (SPS)
            2 = DGPS fix
            3 = PPS fix
    		4 = Real Time Kinematic
    		5 = Float RTK
            6 = estimated (dead reckoning) (2.3 feature)
    		7 = Manual input mode
    		8 = Simulation mode
        num_sats: number of satellites being tracked
        hdp: Horizontal dilution of position
        alt: Altitude, Meters, above mean sea level
        geoid_height: Height of geoid (mean sea level) above WGS84 ellipsoid
        checkum: message checksum
    '''

    def __init__(self, inputString=''):
        s = inputString.split(',')
        if not len(s) == 15 or not s[0] == '$GPGGA':
            raise ValueError('Invalid input string for NMEA GGA object, given string was: ' + inputString)
        else:
            try:
                self.time = s[1]
                self.lat = float(s[2][:2]) + float(s[2][2:])/60
                if(s[3] == 'S'):
                    self.lat = -1 * self.lat
                self.lng = float(s[4][:3]) + float(s[4][3:])/60
                if(s[5] == 'W'):
                    self.lng = -1 * self.lng
                self.fix_quality = s[6]
                self.num_sats = int(s[7])
                self.hdp = float(s[8])
                self.alt = float(s[9])
                self.geoid_height = float(s[11])
                self.checksum = s[14]
            except ValueError:
                if not len(self.time):
                    self.time = ''
                if not hasattr(self, 'lat') or not self.lat:
                    self.lat = 0.0
                if not hasattr(self, 'lng') or not self.lng:
                    self.lng = 0.0
                if not hasattr(self, 'fix_quality') or not self.fix_quality:
                    self.fix_quality = 0
                if not hasattr(self, 'num_sats') or not self.num_sats:
                    self.num_sats = 0
                if not hasattr(self, 'hdp') or not self.hdp:
                    self.hdp = 0.0
                if not hasattr(self, 'alt') or not self.alt:
                    self.alt = 0.0
                if not hasattr(self, 'geoid_height') or not self.geoid_height:
                    self.geoid_height = 0.0
                if not hasattr(self, 'checksum') or not self.checksum:
                    self.checksum = ''

    def getPoint(self):
        '''
        Returns a Point version of itself
        '''
        return Point(self.lat, self.lng, self.alt)

def getNMEA(line):
    '''
    Given a line, tries to make a NMEA object from it, or returns None.
    Args:
        line: NMEA sentence
    Returns:
        NMEA object if valid line (eg. GGA), None if not valid
    '''
    if not line:
        return None
    else:
        s = line.split(',')
        if len(s) == 15 and s[0] == '$GPGGA':
            return GGA(line)
        else:
            return None
