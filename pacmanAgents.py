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
from ann import Ann
import random
import game
import util
import time 



class ANNAgent(Agent):
    "An agent that uses an ANN with 5x5 grid around pacman and outputs a direction to go"

    def getGrid(self, state): 
        #Function that parses through the state to extract:
        #    -pacmans position
        #    -ghost position
        #    -food positions
        #    -capsule positions
        #    -start of the grid
        # -it then populates the grid based on the parsing"

        pacman_position = state.getPacmanPosition()
        grid_start = [pacman_position[0]-2,pacman_position[1]-2]
        ghost1 = [state.getGhostPosition(1)[0] - grid_start[0], state.getGhostPosition(1)[1] - grid_start[1] ]
        ghost2 = [state.getGhostPosition(2)[0] - grid_start[0], state.getGhostPosition(2)[1] - grid_start[1] ]
        food = state.getFood() 
        capsules = state.getCapsules()
        walls = state.getWalls();


        # Populating the grid with walls,pellets, and out of bound: @@@
        #   -starting at the starting position(pacman's row-2 pacman's col-2)
        grid = []
        for col in range(0,5):
            grid.append([]) #append a list to the grid 5 times(making an empty 2d list)
            for row in range(0,5):
                #checks for out of bound locations, making '&' if it the spot is out 
                if ( (row + grid_start[1]) >= len(walls[0]) ) or ( (col + grid_start[0]) >= 20 ) or ( (row + grid_start[1]) < 0 ) or ( (col + grid_start[0]) <0 ):
                    grid[col].append('&') # out of bounds
                else:
                    #
                    if walls[ col+grid_start[0] ][ row+grid_start[1] ] == True:
                        grid[col].append('%')# wall 
                    elif food[ col+grid_start[0] ][ row+grid_start[1] ] == True:
                        grid[col].append('o')# pellet
                    else:
                        grid[col].append(' ')# empty space


        grid[2][2] = '@' #pacman location(always in the middle)
        #add both ghost to grid if position is inside grid range 
        if ghost1[0] < 5 and ghost1[1] < 5 and ghost1[0] > -1 and ghost1[1] > -1:
            grid[int(ghost1[0])][int(ghost1[1])] = 'X'
        if ghost2[0] < 5 and ghost2[1] < 5 and ghost2[0] > -1 and ghost2[1] > -1:
            grid[int(ghost2[0])][int(ghost2[1])] = 'X'

        #iterates through capsule list and adds if position is inside grid range
        for i in range(0,len(capsules)):
            distance = [capsules[i][0] - grid_start[0], capsules[i][1]-grid_start[1] ]
            if distance[0] < 5 and distance[1] < 5 and distance[0] > -1 and distance[1] > -1:
                grid[distance[0]][distance[1]] = '0'



        return grid


    def getAction(self, state):#pass all game state
        "The agent receives a GameState (defined in pacman.py)."

        grid = self.getGrid(state)
  
        #1d array to pass as input to ANN
        input_ = []
        for col in range(4,-1,-1):
            for row in range(0,5):
                input_.append(grid[row][col])

        del input_[12]# we don't need the square pacman is in...
        arrayForAnn = []

        #Python does not have a switch statement, so I just created function for mapping these
        # Alternatively we could use a Dictionary/Hash Table
        # Should only ever return one of the values inside {}, not 1.337
        def switch_statement(argument):
            switcher = {
                '& ': 0.99, # OutOfBounds
                '% ': 0.90, # Wall
                'X ': 0.75, # Ghost
                '  ': 0.50, # Empty
                'o ': 0.25, # Food
                '0 ': 0.20, # Capsule
            }
            return switcher.get(argument, 1.337)

        for symbolicNonsense in input_:
            arrayForAnn.append(switch_statement(symbolicNonsense))
            
        myAnn = Ann()
        predictedDirection = myAnn.processInput(arrayForAnn)
        #legal = state.getLegalPacmanActions()

        #if predictedDirection in state.getLegalPacmanActions():
        if predictedDirection in state.getLegalPacmanActions():
            #return predictedDirection
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
