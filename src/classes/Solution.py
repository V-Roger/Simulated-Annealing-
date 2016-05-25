# Solution.py
#------------
# One solution to the Simulated Annealing problem
#------------

import random

class Solution:

	def __init__(self, _sc = []):
		self.solutionCenters = _sc

	def getValue():
		value = 0.0
		for center in self.solutionCenters:
			value += center.getCost()

		return value

	def addSolutionCenter(_sc):
		if !_sc in self.solutionCenters:
			self.solutionCenters.append(_sc)

	def generateNeighbour():
		neighbour = Solution(self.solutionCenters)
		
		randomOriginCenter = random.choice(neighbour.solutionCenters)
		furthestAgency = randomOriginCenter.popAgency()
		
		randomTargetCenter = random.choice(neighbour.solutionCenters)
		while !randomTargetCenter.canAddAgency(furthestAgency):
			randomTargetCenter = random.choice(neighbour.solutionCenters)

		randomTargetCenter.addAgency(furthestAgency)
		
		return neighbour