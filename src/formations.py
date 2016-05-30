# -*-coding:Latin-1 -*
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

import copy as copy
import random as random
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from time import time


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
    dType = np.empty((0,), dtype=[('lat', np.float32), ('lon', np.float32), ('area', np.float32), ('color', np.str_, 7)])

    solutionCenters = solution.getSolutionCenters()

    solutionMap = np.ndarray(shape=(0,3), dtype=dType.dtype)
    solutionAgenciesMap = np.ndarray(shape=(0,3), dtype=dType.dtype)

    i = 0

    usedColors = []

    for center in solutionCenters:
        if len(center.getAgencies()) > 0:
            color = "#%06x" % random.randint(0, 0xFFFFFF)
            while color in usedColors:
                color = "#%06x" % random.randint(0, 0xFFFFFF)

            usedColors.append(color)
            i += 1
            area = (np.pi * (5 * center.getNbTrainees()) ** 2) / 20
            added = tuple([center.getCenter().getLatitude(), center.getCenter().getLongitude(), area, color])
            solutionMap = np.append(solutionMap, np.array([added], dtype=dType.dtype))

            for agency in center.getAgencies():
                solutionAgenciesMap = np.append(solutionAgenciesMap, np.array([tuple([agency.getLatitude(), agency.getLongitude(), 10.0, color])], dtype=dType.dtype))

    themap = Basemap(projection='gall',
                  llcrnrlon = -5,              # lower-left corner longitude
                  llcrnrlat = 40,               # lower-left corner latitude
                  urcrnrlon = 10,               # upper-right corner longitude
                  urcrnrlat = 55,               # upper-right corner latitude
                  resolution = 'f',
                  area_thresh = 100000.0,
                  )

    themap.drawcoastlines()
    themap.drawcountries()
    themap.fillcontinents(color='gainsboro')
    themap.drawmapboundary(fill_color='steelblue')

    ax, ay, aa, ac = solutionAgenciesMap['lon'], solutionAgenciesMap['lat'], solutionAgenciesMap['area'], solutionAgenciesMap['color']

    x, y, a, c = solutionMap['lon'], solutionMap['lat'], solutionMap['area'], solutionMap['color']
    # themap.plot(x, y,
    #             'o',                    # marker shape
    #             color=solutionMap['color'],                # marker colour
    #             markersize=4            # marker size
    #             )

    themap.scatter(ax, ay, latlon=True, s=aa, color=ac, zorder=9)
    themap.scatter(x, y, latlon=True, s=a, color=c, zorder=10, marker="s")

    plt.show()

print 'Load agencies ...'
agencies = readAgencies()
number = 0
for agency in agencies:
    number += agency.getNbTrainees()
print('{numberAgencies} agencies loaded with {numberTrainees} trainees'.format(numberAgencies=len(agencies), numberTrainees=number))
print 'Load centers ...'
centers = readCenters()
print('{numberCenters} centers loaded'.format(numberCenters=len(centers)))

print 'Initialization ...'
startSolution = Solution()

startAgencies = copy.deepcopy(agencies)

for center in centers:
    solutionCenter = SolutionCenter(center)
    startSolution.addSolutionCenter(solutionCenter)

while len(startAgencies) > 0:
    agency = random.choice(startAgencies)
    startAgencies.remove(agency)

    startAgencies = copy.deepcopy(startAgencies)

    solutionCenter = random.choice(startSolution.getSolutionCenters())
    while not solutionCenter.canAddAgency(agency):
        solutionCenter = random.choice(startSolution.getSolutionCenters())
            
    solutionCenter.addAgency(agency)
#endwhile
initialTemp = 2000
nbTempChanges = 100
nbSteps = 10
neighbourGeneration = 5
mu = 0.70
sa = SimulatedAnnealing()
print('Start simulated annealing with following parameters:\n Start temperature: {t0}\n # change of temperature: {tempChanges}\n # steps by temperature: {steps}\n Mu (temperature decay): {mu}\n Neighbouring factor: {neighbour}\n...'.format(
    t0=initialTemp, tempChanges=nbTempChanges, steps=nbSteps, neighbour=neighbourGeneration, mu=mu
))
t0 = time()
#solution initiale, temperature initiale, nombre de changement de temperature, nombre d'iteration par palier de temperature, nombre maximum d'agences à enlever d'un centre,mu
optimisedSolution = sa.run(startSolution, initialTemp, nbTempChanges, nbSteps, neighbourGeneration, mu)
t1 = time()

print('End simulated annealing\nMinimum cost found: {solution}\nExecution time: {time}'.format(solution=optimisedSolution.getValue(), time=(t1-t0)))
plt.plot(sa.getLog())

plt.show()
displayMap(optimisedSolution)

numberAgencies = 0
numberCenters = 0
numberTrainees = 0
for solutionCenter in optimisedSolution.getSolutionCenters():
    if (solutionCenter.getNbTrainees() > 0):
        numberCenters += 1
        numberAgencies += len(solutionCenter.getAgencies())
        numberTrainees += solutionCenter.getNbTrainees()

print('{trainees} trainees from {agencies} agencies are dispatch in {centers} centers'.format(trainees=numberTrainees, agencies=numberAgencies, centers=numberCenters))

#build worst solution for comparison
# agencies = readAgencies()
# worstSolution = Solution()
# for center in centers:
#     solutionCenter = SolutionCenter(center)
#     worstSolution.addSolutionCenter(solutionCenter)
# #endfor

# for agency in agencies:
#     furthestSolutionCenter = None
#     furthestDist = 0
#     for solutionCenter in worstSolution.getSolutionCenters():
#         if solutionCenter.canAddAgency(agency) & (agency.getDistanceTo(solutionCenter.getCenter()) > furthestDist):
#             if not furthestSolutionCenter is None:
#                 furthestSolutionCenter.removeAgency(agency)
#             #endif
#             solutionCenter.addAgency(agency)
#             furthestDist = agency.getDistanceTo(solutionCenter.getCenter())
#         #endif
#     #endfor 
# #endfor

# print worstSolution.getValue()
