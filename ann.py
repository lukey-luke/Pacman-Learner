import math

class Neuron:
    def __init__(self):
        self.aVal    = 0
        self.delta   = 0
        self.weights = 0

class Ann:
    "A container with a last-in-first-out (LIFO) queuing policy."
    def __init__(self):
        self.data = [][] #where the actual ann's neurons go
        self.m_numIterations =0
        self.m_alpha =0
        self.inputs  = []

    # Iterate through input layer a_j = x_j
    def step1(self, listOfInputs):
        for i in listOfInput:
            self.data[i][0] = listOfInput[i]

    # Iterate through input layer rest of layers to assign a_j
    def step2and3(self, listOfInputs):
        for j in range(1,len(listOfInputs)):
            for i in range(0,len(listOfInputs[j]):
                    in_j = 0
                    for k in listOfInputs[j-1]
                        in_j += self.data[j-1][k].aVal * self.data[j-1][k].weights[i]

                    self.data[j][i].aVal = 1 / (1 + exp(-1 * in_j)




