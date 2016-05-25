# SolutionCenter.py
#------------------
# An entity representing the association of a Center with 0..n Agencies
#------------------

class SolutionCenter:

    COST_BY_KM = 0.4

    def __init__(self, _center):
        self.center = _center
        self.agencies = []
        self.nbTrainees = 0
        self.value = 0.0

    def getCenter(self):
        return self.center

    def getAgencies(self):
        return self.agencies

    # adds an agency in the list, sorted by distance from the training center (ASC)
    def addAgency(self, _a):
        if self.canAddAgency(_a):
            idx = 0
            idMax = len(self.agencies) - 1
            if(idMax > 0) :
                while (idx < idMax) & (_a.getDistanceTo(self.center) < self.agencies[idx].getDistanceTo(self.center)):
                    idx += 1

            self.agencies.insert(idx, _a)
            self.nbTrainees += _a.getNbTrainees()
            self.updateValue(_a)

    def removeAgency(self, _a):
        if _a in self.agencies:
            self.agencies.remove(_a)     
            self.nbTrainees -= _a.getNbTrainees()
            self.updateValue(_a, -1)

    def canAddAgency(self, _a):
        return ((self.nbTrainees + _a.nbTrainees) <= self.center.MAX_TRAINEES) & (_a not in self.agencies)

    # removes the agency furthest away from the training center and returns it
    def popAgency(self):
        agency = self.agencies.pop()
        self.updateValue(agency, -1)
        self.nbTrainees -= agency.getNbTrainees()
        return agency

    def getNbTrainees(self):
        return self.nbTrainees

    def getValue(self):
        return self.value

    def updateValue(self, _a, sign = 1):
        self.value = self.value + sign * (_a.getNbTrainees() * self.COST_BY_KM  * _a.getDistanceTo(self.center))

    def getCost(self):
        return self.value if self.value == 00 else self.center.BASE_COST + self.value

