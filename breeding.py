from ann import Ann
import operator
from ann import Neuron

MUTATION_CHANCE = .0018382353 # 1 / number of weights in ann
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

   def getNextGeneration(self):
      sorted_ = sorted(self.data, key=operator.attrgetter('highScore'), reverse=True)
      nextGeneration = [] 
      #keep 8 best parents from last generation
      for i in range(0, len(sorted_)/2):
         nextGeneration.append(sorted_[i])

      #add 1 child bred from fittest parents
      child = self.annBreeding(nextGeneration[0], nextGeneration[1])
      nextGeneration.append(child)

      #add other 7 children bred from rest of parents
      for i in range(0, len(nextGeneration) - 1):
         child = self.annBreeding(nextGeneration[i], nextGeneration[i+1])
         nextGeneration.append(child)
      
      #mutate children for nextGeneration
      mutateAnns(nextGeneration)
      self.data = nextGeneration

   
   def mutateAnns(self, nextGen):
      #mutate children
      for i in range(len(nextGen)/2, len(nextGen)): #iterate through ANNs
         for j in range(0, len(nextGen[i].data)): #iterate through layers of ANN
            for k in range(0, len(nextGen[i].data[j])): #iterate through neurons in layer
                  for l in range(0, len(nextGen[i].data[j][k].weights)): #iterate through weights in neuron
                     chance = random.uniform(0, 1) #mutate or not?
                     if chance < MUTATION_CHANCE:
                        plusOrMinus = random.uniform(0, 1)
                        #+ OR - (weight* OR weight/ MUTATION_SCALAR)
                        if plusOrMinus < .5:
                          nextGen[i].data[j][k].weights[l] += nextGen[i].data[j][k].weights[l]/MUTATION_SCALAR
                        else:
                          nextGen[i].data[j][k].weights[l] -= nextGen[i].data[j][k].weights[l]/MUTATION_SCALAR


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

      for i in len(0, len(mom.data) - 1): #iterate through layers
         for j in len(0, len(mom.data[i])): #iterate through neurons
               chance = random.uniform(0, 1); #which parent to get genne from
               if chance < percent:
                  child.data[i][j] = parents[fittest].data[i][j]
               else:
                  child.data[i][j] = parents[notFit].data[i][j]

      return child
