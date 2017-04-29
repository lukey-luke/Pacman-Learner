from ann import Ann
from ann import *
import operator
import random
from random import randint
from ann import Neuron

MUTATION_SCALAR = 5 # weight + weight* or weight/MUTATION_SCALAR
ANN_COUNT = 16 # ANNs we'll store 

class Breeding:
   def __init__(self):
      self.avgScoreOfAnns = 0
      self.highScoreOfAnns = -999
      self.data = [Ann()] * ANN_COUNT

   def updateAvgScore(self):
      avg = 0
      for i in range(0, len(self.data)):
         avg = avg + self.data[i].score
      self.avgScoreOfAnns = avg/len(self.data)

   def updateHighScore(self):
      for i in range(0, len(data)):
         if self.data[i].highScore > self.highScoreOfAnns:
            self.highScoreOfAnns = self.data[i].highScore
   
   def setGen(self, newAnns):
      self.data = newAnns

   def getNextGeneration(self):
      sorted_ = sorted(self.data, key=operator.attrgetter('highScore'), reverse=True)
      nextGeneration = [] 
      #keep 8 best parents from last generation
      for i in range(0, len(sorted_)/2):
         nextGeneration.append(sorted_[i])

      # make array to hold children of next gen
      babies = []
      
      #add 1 child bred from fittest parents
      child = self.annBreeding(nextGeneration[0], nextGeneration[1])
      babies.append(child)

      #Breed children and mutate them
      for i in range(0, len(nextGeneration) - 1):
         child = self.annBreeding(nextGeneration[i], nextGeneration[i+1])
         self.mutateAnn(child)
         babies.append(child)
      
      # adding new children to population
      for i in range(0, len(babies)):
         nextGeneration.append(babies[i])
      
      #saving the generation
      self.data = nextGeneration
   
   def mutateAnn(self, nextGen):
      layer = randint(0, NUM_OF_LAYERS - 2) #choose layer from nextGen ANN, -2 because we dont want to access output layer
      neuron = randint(0, len(nextGen.data[layer]) - 1) #choose neuron from that layer
      weight = randint(0, len(nextGen.data[layer][neuron].weights) - 1) #choose weight from that neuron
      plusOrMinus = random.uniform(0,1)
      if plusOrMinus > .5:
          nextGen.data[layer][neuron].weights[weight] += nextGen.data[layer][neuron].weights[weight] / MUTATION_SCALAR
      else:
          nextGen.data[layer][neuron].weights[weight] -= nextGen.data[layer][neuron].weights[weight] / MUTATION_SCALAR


   def annBreeding(self, mom, dad):
      child = Ann() 
      momScore = mom.highScore
      dadScore = dad.highScore
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

      for i in range(0, len(mom.data) - 1): #iterate through layers
         for j in range(0, len(mom.data[i])): #iterate through neurons
               chance = random.uniform(0, 1); #which parent to get genne from
               if chance < percent:
                  child.data[i][j] = parents[fittest].data[i][j]
               else:
                  child.data[i][j] = parents[notFit].data[i][j]

      return child
