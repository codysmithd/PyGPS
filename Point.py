'''
Point.py
Defines a class to represent a simple point
'''

class Point:
    '''
    Point: simple coordinate point
    Attributes:
        lat: Latutude (decimal)
        lng: Longitude (decimal)
        alt: Altitude (meters)
    '''

    def __init__(self, lat=0, lng=0, alt=0):
        self.lat = lat
        self.lng = lng
        self.alt = alt

    # Crude distance (in arbitrary units) to another point
    def getDistance(self, toPoint):
        return math.sqrt(math.pow((self.lat - toPoint.lat),2) + math.pow((self.lng - toPoint.lng),2))
