# Agency.py
#----------
# Agency sending people over to get trained
# Extends Location.py
#----------

import Location as location

class Agency(location.Location):

    def __init__(self, _id, _long, _lat, _nbTrainees):
        super(Agency, self).__init__(_id, _long, _lat)
        self.nbTrainees = _nbTrainees

    def getNbTrainees(self):
        return self.nbTrainees