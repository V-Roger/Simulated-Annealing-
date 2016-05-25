# Solution.py
#------------
# One solution to the Simulated Annealing problem
#------------

import random

class Solution:

	def __init__(self, _sc = []):
		self.solutionCenters = _sc

	def getValue(self):
		value = 0.0
		for center in self.solutionCenters:
			value += center.getCost()

		return value

	def getSolutionCenters(self):
		return self .solutionCenters

	def addSolutionCenter(self, _sc):
		if _sc not in self.solutionCenters:
			self.solutionCenters.append(_sc)

	def generateNeighbour(self):
		neighbour = Solution(list(self.solutionCenters))
		
		randomOriginCenter = random.choice(neighbour.solutionCenters)
		while len(randomOriginCenter.agencies) == 0:
			randomOriginCenter = random.choice(neighbour.solutionCenters)

		furthestAgency = randomOriginCenter.popAgency()
		
		randomTargetCenter = random.choice(neighbour.solutionCenters)
		while not randomTargetCenter.canAddAgency(furthestAgency):
			randomTargetCenter = random.choice(neighbour.solutionCenters)

		randomTargetCenter.addAgency(furthestAgency)
		
		return neighbour