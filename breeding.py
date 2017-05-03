from ann import Ann
from ann import *
import operator
import random
from random import randint
from ann import Neuron
import copy

MUTATION_SCALAR = 5 # weight + weight* or weight/MUTATION_SCALAR
ANN_COUNT = 32 # ANNs we'll store 

class Breeding:
    def __init__(self):
        self.data = [Ann()] * ANN_COUNT
        self.highScores = []
        self.avgScores  = []

    def initialize(self):
        chrisMartinez = Ann()
        #chrisMartinez.print()
        #chrisMartinez.printLayer(3)
        """
        for i in range(0, 9):
            chrisMartinez.trainShit()
        """

        self.data[0] = chrisMartinez
        for i in range(1, ANN_COUNT):
            #temp = copy.copy(chrisMartinez) 
            #self.mutateAnn(temp)
            temp = Ann()
            #temp.printAnn()
            self.data[i] = temp

    def updateAvgScore(self):
        avg = 0
        for i in range(0, len(self.data)):
            avg += self.data[i].score
        self.avgScores.append(avg/len(self.data))

    def updateHighScore(self):
        newScore = -9999
        for i in range(0, len(self.data)):
            if self.data[i].highScore > newScore:
                newScore = self.data[i].highScore
        self.highScores.append(newScore)

    def setGen(self, newAnns):
        self.data = newAnns

    def printAvgScore(self):
        print "----------- Averages: ",
        for i in range(0, len(self.avgScores)):
            print self.avgScores[i],

    def getNextGeneration(self):
        sorted_ = sorted(self.data, key=operator.attrgetter('highScore'), reverse=True)#sort anns so highest score is first
        nextGeneration = [] 
        #keep top 50% from last generation
        for i in range(0, len(sorted_)/2):
            nextGeneration.append(sorted_[i])

        # make array to hold children of next gen
        babies = []

        #add 1 child bred from fittest parents
        child = self.annBreeding(nextGeneration[0], nextGeneration[1])
        # average of 1 .mutateAnn() call, but sometimes have up to 3?!??
        # (0-2 mutations ea time)
        self.mutateAnn(child)#mutate child from two fittest parents
        babies.append(child)

        #Breed children and mutate them
        for i in range(0, len(nextGeneration) - 1):
            child = self.annBreeding(nextGeneration[0], nextGeneration[i+1])
            self.mutateAnn(child)
            babies.append(child)

        # adding new children to population
        for i in range(0, len(babies)):
            nextGeneration.append(babies[i])

        self.updateHighScore()
        self.updateAvgScore()

        #saving the generation
        self.data = nextGeneration

    def mutateAnn(self, nextGen):
        layer = randint(0, NUM_OF_LAYERS - 2) #choose layer from nextGen ANN, -2 because we dont want to access output layer
        neuron = randint(0, len(nextGen.data[layer]) - 1) #choose neuron from that layer
        weight = randint(0, len(nextGen.data[layer][neuron].weights) - 1) #choose weight from that neuron

        """
        Old way relied on previous value and either incremented or decremented
        """
        #new mutation weights need to be large enough to make a difference
        nextGen.data[layer][neuron].weights[weight] += random.uniform(-1.2, 1.2)

        """
        #TODO mess w/ this range try new numbers
        newWeight  = random.uniform(-1.2, 1.2)
        nextGen.data[layer][neuron].weights[weight] = newWeight
        """


    # mom and dad are two anns that are being bred
    def annBreeding(self, mom, dad):
        child = Ann() 
        momScore = mom.highScore
        dadScore = dad.highScore
        print "momScore: ", momScore, " and dadScore: ", dadScore
        total = momScore + dadScore
        parents = [mom, dad] #parents in array for easier indexing

        #choosing fittest parents, so they pass their genes more often
        if momScore > dadScore: 
           percent = momScore/total
           fittest = 0
           notFit = 1
        else:
            percent = dadScore/total
            fittest = 1
            notFit = 0

        #TODO try swapping weights instead of entire neurons
        for i in range(0, len(mom.data) - 1): #iterate through layers
            for j in range(0, len(mom.data[i])): #iterate through neurons
                chance = random.uniform(0, 1); #which parent to get genne from
                if chance < percent:
                    child.data[i][j] = parents[fittest].data[i][j]
                else:
                     child.data[i][j] = parents[notFit].data[i][j]

        return child

