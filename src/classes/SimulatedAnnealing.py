# SimulatedAnnealing.py
#----------------------
# Provides the algorithm to perform a simulated annealing search
#----------------------

import random
import math
import copy
import sys

class SimulatedAnnealing:

    def __init__(self):
        self.log = []

    def getLog(self):
        return self.log

    def progress(self, count, total, status=''):
        bar_len = 60
        filled_len = int(round(bar_len * count / float(total)))

        percents = round(100.0 * count / float(total), 1)
        bar = '=' * filled_len + '-' * (bar_len - filled_len)

        sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
        sys.stdout.flush()  # As suggested by Rom Ruben (see: http://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console/27871113#comment50529068_27871113)


    # _initialTemp : 
    # _nbTempChanges : 
    # _nbSteps : 
    def run(self, _start, _initialTemp, _nbTempChanges, _nbSteps, _neighbourGeneration, _mu):
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

                self.progress( j + i * _nbSteps, _nbSteps * _nbTempChanges)

            # endfor j

            temperature = self.tempDecayal(temperature, _mu)

        # endfor i

        return solMin
    
    # Temperature decayal function
    def tempDecayal(self, _t, _mu):
        return _mu * _t