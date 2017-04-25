import math
from random import randint
from pacmanAgents import Directions
LENGTH_OF_INPUT  = 24
LENGTH_OF_OUTPUT = 4
NUM_OF_LAYERS    = 2

#Enumish things
ghost   = 1
blank   = 2
wall    = 3
food    = 4
capsule = 5
oob     = 6

class Neuron:
    def __init__(self):
        self.aVal    = 0
        #self.delta   = 0
        self.weights = []
        for i in range(0, LENGTH_OF_OUTPUT)):# right when we have a neuron, give it 4 rand wghts
            self.weights.append( random.uniform(0.1, 1.9) ) # @@@


class Ann:
    def __init__(self):
        self.data = [][] #where the actual ann's neurons go
        self.m_numIterations =0
        self.m_alpha =0
        self.inputs  = []
        for i in LENGTH_OF_INPUT:
            temp = Neuron()
            self.data[].append(temp)

    def processInput(self, listOfInputs):
        step1(listOfInputs)
        step2and3(listOfInputs)
        return getDirection()

    # Iterate through input layer a_j = x_j
    def step1(self, listOfInputs):
        for i in listOfInput:
            self.data[i][0].aVal = listOfInput[i]

    # Iterate through input layer rest of layers to assign a_j
    def step2and3(self, listOfInputs):
        for j in range(1,len(listOfInputs)):
            for i in range(0,len(listOfInputs[j]) ):
                in_j = 0
                    for k in listOfInputs[j-1]:
                        in_j += self.data[j-1][k].aVal * self.data[j-1][k].weights[i]

                    self.data[j][i].aVal = 1 / (1 + exp(-1 * in_j)

                            # Look at output layer and figure out which direction it is saying to go
                            def getDirection(self):
                            maxVal = -9999
                            direction = Directions.LEFT
                            for i in range(1,4): # for ea node in output layer...
                            if data[NUM_OF_LAYERS -1][i].aVal > maxVal:







