import random
from math import exp
from math import sqrt
from game import Directions
LENGTH_OF_INPUT  = 96
LENGTH_OF_OUTPUT = 4
NUM_OF_LAYERS    = 4
ALPHA_VALUE      = 0.01

class Neuron:
    def __init__(self):
        self.aVal    = 0
        self.delta   = 0
        self.weights = []
        #for i in range(0, LENGTH_OF_OUTPUT)):# right when we have a neuron, give it 4 rand wghts
        #    self.weights.append( random.uniform(0.1, 1.9) ) # @@@


#A good majorify of fxns should just access data[][], as that is where the neurons are stored
class Ann:
    """
    .___       .__.__  __  .__       .__  .__                __  .__
    |   | ____ |__|__|/  |_|__|____  |  | |__|____________ _/  |_|__| ____   ____
    |   |/    \|  |  \   __\  \__  \ |  | |  \___   /\__  \\   __\  |/  _ \ /    \
    |   |   |  \  |  ||  | |  |/ __ \|  |_|  |/    /  / __ \|  | |  (  <_> )   |  \
    |___|___|  /__|__||__| |__(____  /____/__/_____ \(____  /__| |__|\____/|___|  /
             \/                    \/              \/     \/                    \/
    """
    def __init__(self):
        self.data = [[] for l in range(NUM_OF_LAYERS)] #where the actual ann's neurons go
        self.m_numIterations =0
        self.m_alpha =0
	self.name = ""
        self.inputs  = []
        self.encodings = [#Euclidean distnaces are calculated from these encodings to determine direction
                    # try encodings for .8 .2 .2 .2
                    [0.9, 0.1, 0.1, 0.1], #North
                    [0.1, 0.9, 0.1, 0.1], #East
                    [0.1, 0.1, 0.9, 0.1], #South
                    [0.1, 0.1, 0.1, 0.9]  #West
                ]
        self.directionMapping = [#These are the actual directions of type that Pacman understands
                Directions.NORTH,
                Directions.EAST,
                Directions.SOUTH,
                Directions.WEST
                ]
        self.netStructure = [LENGTH_OF_INPUT, 48, 48, LENGTH_OF_OUTPUT]#just used to describe structure
        self.constructNetwork()
        self.score     = -9999#last score achieved by this ANN
        self.highScore = -9999#highest score ever achieved by ANN

    #This function assigns neurons to elements of the 2d array,
    # ea containing a list of weights initialized to 0.1
    def constructNetwork(self):
        for i in range( 0, len(self.netStructure) ):# for layer i out of all layers
            tempList = []

            for neuronNum in range(0, self.netStructure[i]):
                tempNeuron = Neuron()

                if i < len(self.netStructure)-1:#create list of wghts corresponding to num neurons in next layer
                    for j in range(0, self.netStructure[i+1]):
                        weight = random.uniform(-4.5, 4.5)# this should be needed
                        tempNeuron.weights.append(weight)
                #tempNeuron.weights = [0.1] * self.netStructure[i+1]
                tempList.append(tempNeuron)

            #tempList = [tempNeuron] * self.netStructure[i]

            self.data[i] = tempList#add newly created layer to network

    # Run steps 1, 2, and 3. Return direction for pacman based on provided input
    def processInput(self, listOfInputs):
        self.step1(listOfInputs)
        self.step2and3()
        return self.getDirection()

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
    # Calculate error for ea node in output layer
    # yVec is the vector of expected outputs - currently a placeholder until we know where this will be stored @@@
    def step4(self, yVec):
        for i in range(1,len(self.data[-1])):# For ea node in output layer...
            self.data[-1][i].delta = self.data[-1][i].aVal * (1 - self.data[-1][i].aVal) * (yVec[i] - self.data[-1][i].aVal)

    # Only used for trainig
    # Calculate nodes' error for ea layer except the output layer
    def step5and6(self):
        for l in range(0, len(self.data)-1):
            for n in range(0, len(self.data[l])):
                newDeltaVal = self.data[l][n].aVal * (1 - self.data[l][n].aVal)
                for w in range(0, len(self.data[l][n].weights)):
                    newDeltaVal += (self.data[l][n].weights[w] * self.data[l+1][w].delta)

                self.data[l][n].delta = newDeltaVal

    # Only used for trainig
    # Recaluclate weights based on error (delta values)
    def step7(self):
        for l in range(0, len(self.data)):
            for n in range(0, len(self.data[l])):
                for w in range(0, len(self.data[l][n].weights)):
                    newWeight = self.data[l][n].weights[w]
                    newWeight += (ALPHA_VALUE * self.data[l][n].aVal * self.data[l+1][w].delta)

                    self.data[l][n].weights[w] = newWeight

    """
       _____ __________.___
      /  _  \\______   \   |
     /  /_\  \|     ___/   |
    /    |    \    |   |   |
    \____|__  /____|   |___|
            \/
    """
    # Look at output layer and figure out which direction it is saying to go
    # This is bad and just picks the biggest one. It should do euc dist @@@
    def getDirection(self):
        eucDist = 9999
        goThisWay = Directions.LEFT
        for j in range( 0, len(self.data[-1]) ): # loop through all directional encodings
            #print self.data[-1][j].aVal
            if self.getEucDist(j) < eucDist:
                eucDist = self.getEucDist(j)
                goThisWay = self.directionMapping[j]
        return goThisWay

    # Calculate Euclidean distance for output vector vs an encoding vector
    # vecNum is a number 0-3 to specify the vector being compared to
    def getEucDist(self, vecNum):
        eucDist = 0
        for j in range( 0, len(self.data[-1]) ): # for ea node in output layer...
            temp = self.data[-1][j].aVal - self.encodings[vecNum][j]
            temp = temp**2
            eucDist += temp

        return sqrt(eucDist)

    # Update score and (sometimes) highscore
    def setScore(self, newScore):
        self.score = newScore
        if newScore > self.highScore:
            self.highScore = newScore

    # assign a name to the ann
    def giveName(self, n):
	    self.name = n

    # use Chris' training data and run throug steps 1-7
    def trainTheChrisWay( self ):
        nes = open("won1_input.txt").read().splitlines()
        
        newInputData = []
        for i in range(0, len(nes)):
            newInputData.append([])
            for j in range(0, len(nes[0])):
                newInputData[i].append(int (nes[i][j]))
        
        
        
        lines = [line.rstrip('\n') for line in open('won1_labels.txt')]
        labels = []
        for line in lines:
            line = line.strip().split(' ')
            labels.append(line)
        newOuputData = []
        for line in lines:
            number_strings = line.split() # Split the line on runs of whitespace
            numbers = [float(n) for n in number_strings] # Convert to integers
            newOuputData.append(numbers) # Add the "row" to your list.

        for arrNum in range(0, len(newInputData)):
            self.step1(newInputData[arrNum])
            self.step2and3()
            self.step4(newOuputData[arrNum])
            self.step5and6()
            self.step7()

        

    """
    __________        .__        __    ___________
    \______   \_______|__| _____/  |_  \_   _____/__  ___ ____   ______
     |     ___/\_  __ \  |/    \   __\  |    __) \  \/  //    \ /  ___/
     |    |     |  | \/  |   |  \  |    |     \   >    <|   |  \\___ \
     |____|     |__|  |__|___|  /__|    \___  /  /__/\_ \___|  /____  >
                              \/            \/         \/    \/     \/
    """
    def printAnn(self):
	print 
	print self.name, " ", self.highScore
	nodeCount = 0
	nextNode = 0
	hLayNum = 1
	#going thru layers
	for i in range(0 , len(self.data)):
	    print
	    if i == 0:
		print "Input Layer"
	    elif i < len(self.data) - 1:
		print "Hidden Layer ", hLayNum
		hLayNum += 1
	    else:
		print "Output Layer"
	    print
	    nextNode = nodeCount
	    #going thru Neurons
	    for k in range(0, len(self.data[i])):
		nodeCount += 1
		conIter = 1
		print "Node ", nodeCount, "-"
		#going thru Weights
		for l in range(0, len(self.data[i][k].weights)):
	            s = "{}".format(self.data[i][k].weights[l])
		    print "        ----", s, "----> ", nextNode + len(self.data[i]) + conIter
		    conIter += 1
	print "------------- end of ANN ------------"
	print


    def printLayer(self, num):
	    nodeCount = 0
	    for i in range(0, num):
		nodeCount += len(self.data[i])
	    nextNode = 0
	    hLayNum = num
	    if num < len(self.data):
	        print
	        if num == 0:
		    print "Input Layer"
	        elif num < len(self.data) - 1:
		    print "Hidden Layer ", hLayNum
	        else:
		    print "Output Layer"
	        print
	        nextNode = nodeCount
	    #going thru Neurons
	        for k in range(0, len(self.data[num])):
		    nodeCount += 1
		    conIter = 1
		    print "Node ", nodeCount, "-"
		#going thru Weights
		    for l in range(0, len(self.data[num][k].weights)):
	                s = "{}".format(self.data[num][k].weights[l])
		        print "        ----", s, "----> ", nextNode + len(self.data[num]) + conIter
		        conIter += 1


    def printNeuron(self, lNum, nNum):
	nodeCount = 0
	for i in range(0, lNum):
	    nodeCount += len(self.data[i])
	nodeCount += nNum
	if lNum < len(self.data):
	    if nNum < len(self.data[lNum]):
		conIter = 0
		print "Node ", nodeCount, "-"
		#going thru Weights
		for i in range(0, len(self.data[lNum][nNum].weights)):
	            s = "{}".format(self.data[lNum][nNum].weights[i])
		    print "        ----", s, "----> ", nodeCount + len(self.data[lNum]) + conIter
		    conIter += 1

    # prints score data for ANN to STDOUT
    def printScore(self):
        print 'Most recent score: ', self.score
        print 'Highest score: ', self.highScore

    def saveFile(self):
        fileName = "saveData" + self.name + ".txt"
        saveFile = open(fileName, 'w')
        saveFile.truncate()
        counter = 0
        for i in range(0, len(self.data)):
            for j in range(0, len(self.data[i])):
                for k in range(0, len(self.data[i][j].weights)):
                    data = " " + str(self.data[i][j].weights[k])
                    #data = "poo"
                    saveFile.write(data)
                    saveFile.write("\n")
        print "Saved: " + str(self.data[0][0].weights[0])
        saveFile.close()
   
 
    def loadFile(self):
        fileName = "saveData" + self.name + ".txt"
        loadFile = open(fileName, 'rwt')
        print "Before Load: " + str(self.data[0][0].weights[0])
        for i in range(0, len(self.data)):
            for j in range(0, len(self.data[i])):
                for k in range(0, len(self.data[i][j].weights)):
                    data = loadFile.readline()
                    self.data[i][j].weights[k] = float(data)
        print "After Load: " + str(self.data[0][0].weights[0])
        loadFile.close()
        

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

