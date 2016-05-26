# Location.py
#------------
# Abstract class implementing a geographical location
#------------

from math import sin, cos, sqrt, atan2, radians

class Location(object):

    def __init__(self, _id, _long, _lat):
        self.idLoc = _id
        self.longitude = _long
        self.latitude = _lat

    def getId(self):
        return self.idLoc

    def getLongitude(self):
        return self.longitude

    def getLatitude(self):
        return self.latitude

    def getDistanceTo(self, there):

        # approximate radius of the earth (in km)
        R = 6373.0

        dlon = there.getLongitude() - self.getLongitude()
        dlat = there.getLatitude() - self.getLatitude()

        a = sin(dlat / 2)**2 + cos(self.getLatitude()) * cos(there.getLatitude()) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c

        return distance / 1000