# pacmanAgents.py
# ---------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from pacman import Directions
from game import Agent
#from ann import Ann
import random
import game
import util
import time 



class ANNAgent(Agent):
    "An agent that goes West until it can't."

    def getGrid(self, state): 

        pacman_position = state.getPacmanPosition()
        grid_start = [pacman_position[0]-2,pacman_position[1]-2]
        ghost1 = [state.getGhostPosition(1)[0] - grid_start[0], state.getGhostPosition(1)[1] - grid_start[1] ]
        ghost2 = [state.getGhostPosition(2)[0] - grid_start[0], state.getGhostPosition(2)[1] - grid_start[1] ]
        food = state.getFood() 
        capsules = state.getCapsules()

        print(pacman_position)
        print(grid_start)

        walls = state.getWalls();
        grid = []


        for col in range(0,5):
            grid.append([])
            for row in range(0,5):
                if ( (row + grid_start[1]) >= len(walls[0]) ) or ( (col + grid_start[0]) >= 20 ) or ( (row + grid_start[1]) < 0 ) or ( (col + grid_start[0]) <0 ):
                    grid[col].append('& ')
                else:
                    if walls[ col+grid_start[0] ][ row+grid_start[1] ] == True:
                        grid[col].append('% ')
                    elif food[ col+grid_start[0] ][ row+grid_start[1] ] == True:
                        grid[col].append('o ')
                    else:
                        grid[col].append('  ')


        grid[2][2] = '@ '
        if ghost1[0] < 5 and ghost1[1] < 5 and ghost1[0] > -1 and ghost1[1] > -1:
            grid[int(ghost1[0])][int(ghost1[1])] = 'X '
        if ghost2[0] < 5 and ghost2[1] < 5 and ghost2[0] > -1 and ghost2[1] > -1:
            grid[int(ghost2[0])][int(ghost2[1])] = 'X '

        for i in range(0,len(capsules)):
            distance = [capsules[i][0] - grid_start[0], capsules[i][1]-grid_start[1] ]
            if distance[0] < 5 and distance[1] < 5 and distance[0] > -1 and distance[1] > -1:
                grid[distance[0]][distance[1]] = '0 '



        return grid


    def getAction(self, state):#pass all game state
        "The agent receives a GameState (defined in pacman.py)."

        grid = self.getGrid(state)
  
        #1d array to hold pass as input to ANN
        input_ = []
        for col in range(4,-1,-1):
            for row in range(0,5):
                input_.append(grid[row][col])
        myAnn = Ann()
        predictedDirection = myAnn.processInput(input_)
        legal = state.getLegalPacmanActions()

        if predictedDirection in state.getLegalPacmanActions():
            return predictedDirection
        else:
            return Directions.STOP

        #for col in range(4,-1,-1):
        #    for row in range(0,5):
        #        print(grid[row][col]),
        #    print("\n")
        #time.sleep(1)
        

        #for i,a in enumerate(walls):
            #print i, ": ", a


        # 1.) Get the grid.
        # 2.) Input the grid to ANN.
        # 3.) Return the results from ANN.


        """
        legal = state.getLegalPacmanActions()
        current = state.getPacmanState().configuration.direction
        if current == Directions.STOP: current = Directions.NORTH
        left = Directions.LEFT[current]
        if left in legal: return left
        if current in legal: return current
        if Directions.RIGHT[current] in legal: return Directions.RIGHT[current]
        if Directions.LEFT[left] in legal: return Directions.LEFT[left]
        return Directions.STOP
        """

class LeftTurnAgent(game.Agent):
    "An agent that turns left at every opportunity"

    def getAction(self, state):
        legal = state.getLegalPacmanActions()
        current = state.getPacmanState().configuration.direction
        if current == Directions.STOP: current = Directions.NORTH
        left = Directions.LEFT[current]
        if left in legal: return left
        if current in legal: return current
        if Directions.RIGHT[current] in legal: return Directions.RIGHT[current]
        if Directions.LEFT[left] in legal: return Directions.LEFT[left]
        return Directions.STOP

class GreedyAgent(Agent):
    def __init__(self, evalFn="scoreEvaluation"):
        self.evaluationFunction = util.lookup(evalFn, globals())
        assert self.evaluationFunction != None

    def getAction(self, state):
        # Generate candidate actions
        legal = state.getLegalPacmanActions()
        if Directions.STOP in legal: legal.remove(Directions.STOP)

        successors = [(state.generateSuccessor(0, action), action) for action in legal]
        scored = [(self.evaluationFunction(state), action) for state, action in successors]
        bestScore = max(scored)[0]
        bestActions = [pair[1] for pair in scored if pair[0] == bestScore]
        return random.choice(bestActions)

def scoreEvaluation(state):
    return state.getScore()
