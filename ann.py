import random
from math import exp
from math import sqrt
from game import Directions
LENGTH_OF_INPUT  = 96
LENGTH_OF_OUTPUT = 4
NUM_OF_LAYERS    = 5

class Neuron:
    def __init__(self):
        self.aVal    = 0
        #self.delta   = 0
        self.weights = []
        #for i in range(0, LENGTH_OF_OUTPUT)):# right when we have a neuron, give it 4 rand wghts
        #    self.weights.append( random.uniform(0.1, 1.9) ) # @@@


#A good majorify of fxns should just access data[][], as that is where the neurons are stored
class Ann:
    """
    .___       .__  __  .__       .__  .__                __  .__               
    |   | ____ |__|/  |_|__|____  |  | |__|____________ _/  |_|__| ____   ____  
    |   |/    \|  \   __\  \__  \ |  | |  \___   /\__  \\   __\  |/  _ \ /    \ 
    |   |   |  \  ||  | |  |/ __ \|  |_|  |/    /  / __ \|  | |  (  <_> )   |  \
    |___|___|  /__||__| |__(____  /____/__/_____ \(____  /__| |__|\____/|___|  /
             \/                 \/              \/     \/                    \/ 
    """
    def __init__(self):
        self.data = [[] for l in range(NUM_OF_LAYERS)] #where the actual ann's neurons go
        self.m_numIterations =0
        self.m_alpha =0
        self.inputs  = []
        self.encodings = [#Euclidean distnaces are calculated from these encodings to determine direction
                    [0.1, 0.1, 0.1, 0.9], #North
                    [0.1, 0.1, 0.9, 0.1], #East
                    [0.1, 0.9, 0.1, 0.1], #South
                    [0.9, 0.1, 0.1, 0.1]  #West
                ]
        self.directionMapping = [#These are the actual directions of type that Pacman understands
                Directions.NORTH,
                Directions.EAST,
                Directions.SOUTH,
                Directions.WEST
                ]
        self.netStructure = [LENGTH_OF_INPUT, 16, 8, 4, LENGTH_OF_OUTPUT]#just used to describe structure
        self.constructNetwork()
        self.score     = -1#last score achieved by this ANN
        self.highScore = -1#highest score ever achieved by ANN

    #This function assigns neurons to elements of the 2d array,
    # ea containing a list of weights initialized to 0.1
    def constructNetwork(self):
        for i in range( 0, len(self.netStructure) ):# for layer i out of all layers
            tempList = []

            for neuronNum in range(0, self.netStructure[i]):
                tempNeuron = Neuron()

                if i < len(self.netStructure)-1:#create list of wghts corresponding to num neurons in next layer
                    for j in range(0, self.netStructure[i+1]):
                        weight = random.uniform(-0.9, 1.9)# this should be needed
                        tempNeuron.weights.append(weight)
                #tempNeuron.weights = [0.1] * self.netStructure[i+1]

                tempList.append(tempNeuron)
            #tempList = [tempNeuron] * self.netStructure[i]

            self.data[i] = tempList#add newly created layer to network

    """
     _______          __                       __       _________ __
     \      \   _____/  |___  _  _____________|  | __  /   _____//  |_  ____ ______  ______
     /   |   \_/ __ \   __\ \/ \/ /  _ \_  __ \  |/ /  \_____  \\   __\/ __ \\____ \/  ___/
    /    |    \  ___/|  |  \     (  <_> )  | \/    <   /        \|  | \  ___/|  |_> >___ \
    \____|__  /\___  >__|   \/\_/ \____/|__|  |__|_ \ /_______  /|__|  \___  >   __/____  >
            \/     \/                              \/         \/           \/|__|       \/
    """
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

    # Only used for trainig
    def step4(self):
        for l in range(1,len(self.data)):# For ea layer 1...L
            for j in range(0,len(self.data[l]) ):# for ea node j in layer l
                in_j = 0
                for neuron in self.data[l-1]:# look a neurons from layer (l-1)
                    in_j += neuron.aVal * neuron.weights[j]

                self.data[l][j].aVal = 1 / (1 + exp(-1 * in_j))

    """
       _____ __________.___
      /  _  \\______   \   |
     /  /_\  \|     ___/   |
    /    |    \    |   |   |
    \____|__  /____|   |___|
            \/
    These are function that are called externally or helper functions for
      functions that are called externally.
    """
    # Run steps 1, 2, and 3. Return direction for pacman based on provided input
    def processInput(self, listOfInputs):
        self.step1(listOfInputs)
        self.step2and3()
        return self.getDirection()

    # Calculate Euclidean distance for output vector vs an encoding vector
    # vecNum is a number 0-3 to specify the vector being compared to
    def getEucDist(self, vecNum):
        eucDist = 0
        for j in range( 0, len(self.data[-1]) ): # for ea node in output layer...
            temp = self.data[-1][j].aVal - self.encodings[vecNum][j]
            temp = temp**2
            eucDist += temp

        return sqrt(eucDist)

    # Look at output layer and figure out which direction it is saying to go
    # This is bad and just picks the biggest one. It should do euc dist @@@
    def getDirection(self):
        eucDist = 9999
        goThisWay = Directions.LEFT
        for j in range( 0, len(self.data[-1]) ): # for ea node in output layer...
            if self.getEucDist(j) < eucDist:
                eucDist = self.getEucDist(j)
                goThisWay = self.directionMapping[j]
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

