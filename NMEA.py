'''
NMEA.py
Defines NMEA sentence classes
'''

import Point

class GGA :
    '''
    NMEA GGA: fix data
    Attributes:
        time: String with UTC time
        lat: Latitude (decimal value)
        lng: Longitude (decimal value)
        fix_quality:
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
            self.time = s[1]
            self.lat = float(s[2][:2]) + float(s[2][2:])/60
            if(s[3] == 'S'):
                self.lat = -self.lat
            self.lng = float(s[4][:3]) + float(s[4][3:])/60
            if(s[5] == 'E'):
                self.lng = -self.lng
            self.fix_quality = s[6]
            self.num_sats = int(s[7])
            self.hdp = float(s[8])
            self.alt = float(s[9])
            self.geoid_height = float(s[11])
            self.checksum = s[14]

    # Returns Point from self
    def getPoint(self):
        return Point(self.lat, self.lng, self.alt)
