# SimulatedAnnealing.py
#----------------------
# Provides the algorithm to perform a simulated annealing search
#----------------------

import random
import math
import copy

class SimulatedAnnealing:

    def __init__(self):
        self.log = []

    def getLog(self):
        return self.log

    # _initialTemp : 
    # _nbTempChanges : 
    # _nbSteps : 
    def run(self, _start, _initialTemp, _nbTempChanges, _nbSteps, _neighbourGeneration):
        solMin = current = _start
        minValue = currentValue = _start.getValue()
        temperature = _initialTemp

        for i in range(0, _nbTempChanges):

            for j in range(0, _nbSteps):

                new = current.generateNeighbour(_neighbourGeneration)
                newValue = new.getValue()
                delta = newValue - currentValue

                self.log.append(newValue)
                
                if delta <= 0:
                # new is a better solution than current
                    current = copy.deepcopy(new)
                    currentValue = newValue
                    if currentValue <= minValue:
                        minValue = currentValue
                        solMin = copy.deepcopy(current)
                else:
                # new is a worse solution than current
                    annealing = random.uniform(0,1)
                    if annealing < math.exp( -(delta) / temperature ):
                        current = copy.deepcopy(new)
                        currentValue = newValue

            # endfor j

            temperature = self.tempDecayal(temperature)

            #print current.getValue()

        # endfor i

        return solMin
    
    # Temperature decayal function
    def tempDecayal(self, _t):
        return 0.95 * _t
