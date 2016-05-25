# formations.py
#--------------
# Uses simulated annealing to solve a problem associating a large number of agencies 
# with an unknown number of formation centers at the lowest possible cost.
#--------------

from classes.Location import Location
from classes.Agency import Agency
from classes.Center import Center
from classes.Solution import Solution
from classes.SolutionCenter import SolutionCenter
from classes.SimulatedAnnealing import SimulatedAnnealing

import random as random
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap


def readAgencies():

	with open('data/agencies.txt') as f:
		agenciesData = f.readlines()
	
	agencies = []

	for agency in agenciesData :
		data = agency.strip().split(';')

		agencies.append(Agency(data[0], float(data[3]), float(data[4]), float(data[5])))

	return agencies

def readCenters():
	with open('data/centers.txt') as f:
		centersData = f.readlines()
	
	centers = []

	for center in centersData :
		data = center.strip().split(';')

		centers.append(Center(data[0], float(data[3]), float(data[4])))

	return centers

def displayMap(solution):
	agenciesMap = np.genfromtxt("data/agencies.txt",
                         delimiter=';', 
                         dtype=[('lat', np.float32), ('lon', np.float32)], 
                         usecols=(4, 5))

	dType = np.empty((0,),
                       dtype=[('lat', np.float32), ('lon', np.float32), ('color', np.str)])

	solutionCenters = solution.getSolutionCenters()

	solutionMap = np.ndarray(shape=(1, 3),
							dtype=dType.dtype)

	i = 0

	for center in solutionCenters:
		color = "#%06x" % random.randint(0, 0xFFFFFF)
		if len(center.getAgencies()) > 0:
			i += 1
			solutionMap = np.append(solutionMap, np.array([tuple([center.getCenter().getLatitude(), center.getCenter().getLongitude(), color])], dtype=dType.dtype))

	fig = plt.figure()

	themap = Basemap(projection='gall',
	              llcrnrlon = -5,              # lower-left corner longitude
	              llcrnrlat = 40,               # lower-left corner latitude
	              urcrnrlon = 10,               # upper-right corner longitude
	              urcrnrlat = 55,               # upper-right corner latitude
	              resolution = 'c',
	              area_thresh = 100000.0,
	              )

	themap.drawcoastlines()
	themap.drawcountries()
	themap.fillcontinents(color = 'gainsboro')
	themap.drawmapboundary(fill_color='steelblue')

	x, y = themap(solutionMap['lon'], solutionMap['lat'])
	themap.plot(x, y, 
	            'o',                    # marker shape
	            color='steelblue',         # marker colour
	            markersize=4            # marker size
	            )

	plt.show()


agencies = readAgencies()
centers = readCenters()
startSolution = Solution()

for center in centers:
	solutionCenter = SolutionCenter(center)
	if len(agencies) > 0:
		agency = agencies.pop()
		print agency.getId
		solutionCenter.addAgency(agency)

	startSolution.addSolutionCenter(solutionCenter)

sa = SimulatedAnnealing()

optimisedSolution = sa.run(startSolution, 0.5, 500, 10)

print optimisedSolution.getValue()

displayMap(optimisedSolution)