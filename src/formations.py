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


agencies = readAgencies()
centers = readCenters()
startSolution = Solution()

for center in centers:
    solutionCenter = SolutionCenter(center)
    if len(agencies) > 0:
        agency = agencies.pop()
        solutionCenter.addAgency(agency)

    startSolution.addSolutionCenter(solutionCenter)

sa = SimulatedAnnealing()

optimisedSolution = sa.run(startSolution, 0.5, 500, 10)

print optimisedSolution.getValue()

displayMap(optimisedSolution)