import random
from math import exp
from game import Directions
LENGTH_OF_INPUT  = 24
LENGTH_OF_OUTPUT = 4
NUM_OF_LAYERS    = 5

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
        #for i in range(0, LENGTH_OF_OUTPUT)):# right when we have a neuron, give it 4 rand wghts
        #    self.weights.append( random.uniform(0.1, 1.9) ) # @@@


class Ann:
    def __init__(self):
        self.data = [[] for l in range(NUM_OF_LAYERS)] #where the actual ann's neurons go
        self.m_numIterations =0
        self.m_alpha =0
        self.inputs  = []
        self.encodings = [
                {0.1, 0.1, 0.1, 0.9}, #North
                {0.1, 0.1, 0.9, 0.1}, #East
                {0.1, 0.9, 0.1, 0.1}, #South
                {0.9, 0.1, 0.1, 0.1}  #West
                ]
        self.directionMapping = [
                Directions.NORTH,
                Directions.EAST,
                Directions.SOUTH,
                Directions.WEST
                ]
        self.netStructure = [LENGTH_OF_INPUT, 16, 8, 4, LENGTH_OF_OUTPUT]
        self.constructNetwork()
        self.score     = -1#last score achieved by this ANN
        self.highScore = -1

#This function assigns neurons to elements of the 2d array,
# ea containing a list of weights initialized to 0.1
    def constructNetwork(self):
        for i in range( 0, len(self.netStructure) ):# for layer i out of all layers
            tempList = []

            for neuronNum in range(0, self.netStructure[i]):
                tempNeuron = Neuron()

                if i < len(self.netStructure)-1:#create list of wghts corresponding to num neurons in next layer
                    for j in range(0, self.netStructure[i+1]):
                        weight = random.uniform(-0.9, 1.9)
                        tempNeuron.weights.append(weight)
                #tempNeuron.weights = [0.1] * self.netStructure[i+1]

                tempList.append(tempNeuron)
            #tempList = [tempNeuron] * self.netStructure[i]

            self.data[i] = tempList#add newly created layer to network

    def processInput(self, listOfInputs):
        print "processing input"
        self.step1(listOfInputs)
        self.step2and3()
        return self.getDirection()

    # Iterate through input layer a_j = x_j
    def step1(self, listOfInputs):
        for i in range( 0, len(listOfInputs) ):
            self.data[0][i].aVal = listOfInputs[i]

    # Iterate through input layer rest of layers to assign a_j
    def step2and3(self):
        for l in range(1,len(self.data)):# For ea layer 1...L
            for j in range(0,len(self.data[l]) ):# for ea node j in layer l
                in_j = 0
                for neuron in self.data[l-1]:# look a neurons from layer (l-1)
                    in_j += neuron.aVal * neuron.weights[j]

                self.data[l][j].aVal = 1 / (1 + exp(-1 * in_j))

    #I can't beleive I am spending time here, but this is for sanity checking that net is O.K.
    def printNetwork(self):
        for j in range( 0, len(self.data) ):
            for i in range( 0, len(self.data[j]) ):
                print 'Neuron in layer ' +j +' node # ' +i +' has following weights: '
                for k  in self.data[j][i].weights:
                    print k 
    # Look at output layer and figure out which direction it is saying to go
    # This is bad and just picks the biggest one. It should do euc dist @@@
    def getDirection(self):
        maxVal = -9999
        goThisWay = Directions.LEFT
        # -1 goes backwards to specify last element in a list
        for j in range( 0, len(self.data[-1]) ): # for ea node in output layer...
            if self.data[-1][j].aVal > maxVal:
                maxVal = self.data[-1][j].aVal
                goThisWay = self.directionMapping[j]
                print "direction set to directionMapping[", j, "]"
        return goThisWay


    # Update score and (sometimes) highscore
    def setScore(self, newScore):
        self.score = newScore
        if newScore > self.highScore:
            self.highScore = newScore



"""
This is some dummy sample code used to test ANN.
myObjy = Ann()
specialArray = [
        0.1,
        0.1,
        0.1,
        0.1,
        0.1,
        0.0,
        0.1,
        0.9,
        0.1,
        0.1,
        0.1,
        0.1,
        0.1,
        0.1,
        0.1,
        0.9,
        0.1,
        0.1,
        0.1,
        0.9,
        0.9,
        0.1,
        0.9,
        0.1
        ]
myObjy.processInput(specialArray)
"""

