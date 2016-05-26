# SimulatedAnnealing.py
#----------------------
# Provides the algorithm to perform a simulated annealing search
#----------------------

import random
import math
import copy

class SimulatedAnnealing:

    # _initialTemp : 
    # _nbTempChanges : 
    # _nbSteps : 
    def run(self, _start, _initialTemp, _nbTempChanges, _nbSteps):
        solMin = current = _start
        minValue = currentValue = _start.getValue()
        temperature = _initialTemp

        for i in range(0, _nbTempChanges):

            for j in range(0, _nbSteps):

                new = current.generateNeighbour()
                newValue = new.getValue()
                delta = newValue - currentValue
                
                if delta <= 0:
                # new is a better solution than current
                    current = new
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

            print minValue

            temperature = self.tempDecayal(temperature)

        # endfor i

        return solMin
    
    # Temperature decayal function
    def tempDecayal(self, _t):
        return 0.95 * _t
