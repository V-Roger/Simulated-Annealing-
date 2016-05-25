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

    def getAgencies():
        return self.agencies

    # adds an agency in the list, sorted by distance from the training center (ASC)
    def addAgency(_a):
        if self.canAddAgency(_a):
            idx = 0
            idMax = len(self.agencies)
            while (idx < idMax) && (_a.getDistanceTo(self.center) < self.agencies[idx].getDistanceTo(self.center)):
                idx++

            self.agencies.insert(idx, _a)
            self.nbTrainees += _a.getNbTrainees
            self.updateValue(_a)

    def removeAgency(_a):
        if _a in self.agencies:
            self.agencies.remove(_a)     
            self.nbTrainees -= _a.getNbTrainees
            self.updateValue(_a, -1)

    def canAddAgency(_a):
        return ((self.nbTrainees + _a.nbTrainees) <= self.center.MAX_TRAINEES) && (!_a in self.agencies)

    # removes the agency furthest away from the training center and returns it
    def popAgency():
        agency = self.agencies.pop()
        self.updateValue(agency, -1)
        self.nbTrainees -= agency.nbTrainees
        return agency

    def getNbTrainees():
        return self.nbTrainees

    def getValue():
        return self.value

    def updateValue(_a, sign = 1):
        self.value = self.value + sign * (_a.getNbTrainees * COST_BY_KM  * _a.getDistanceTo(self.center))

    def getCost():
        return self.value == 0.0 ? self.value : self.center.BASE_COST + self.value

