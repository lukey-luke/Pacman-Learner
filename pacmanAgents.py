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



"An agent that uses an ANN with 5x5 grid around pacman and outputs a direction to go"
class ANNAgent(Agent):
    def __init__(self):
        self.agentAnn = 0#@@@ ensure that self.agentAnn is the same one as the breeder's
        #ensure this is actually changing

    #Set Ann for agent to use every time it calls get action
    #annFromMain is the Ann() passed down by main
    def setAnn(self, annFromMain):
        self.agentAnn = annFromMain

    def getGrid(self, state): 
        #Function that parses through the state to extract:
        #    -pacmans position
        #    -ghost position
        #    -food positions
        #    -capsule positions
        #    -start of the grid
        # -it then populates the grid based on the parsing
        pacman_position = state.getPacmanPosition()
        grid_start = [pacman_position[0]-2,pacman_position[1]-2]
        ghost1 = [state.getGhostPosition(1)[0] - grid_start[0], state.getGhostPosition(1)[1] - grid_start[1] ]
        ghost2 = [state.getGhostPosition(2)[0] - grid_start[0], state.getGhostPosition(2)[1] - grid_start[1] ]
        food = state.getFood() 
        capsules = state.getCapsules()
        walls = state.getWalls()
        grid = []

        #INSERTS 4 NUMBERS INTO EACH CELL OF THE GRID BASED ON WHAT IT SEES
        #   LEGEND:
        #       -wall and out of bound: [0,0,0,1]
        #       -empty spaces: [0,0,1,0]
        #       -pellets and capsules: [0,1,0,0]
        #       -Ghosts: [1,0,0,0]
        #       -Pacman: @ is used as a placeholder, but will be deleted later
        grid = []
        for col in range(0,5):
            grid.append([]) #append a list to the grid 5 times(making an empty 2d list)
            for row in range(0,5):
                #checks for out of bound locations, making '&' if it the spot is out 
                if ( (row + grid_start[1]) >= len(walls[0]) ) or ( (col + grid_start[0]) >= 20 ) or ( (row + grid_start[1]) < 0 ) or ( (col + grid_start[0]) <0 ):
                    grid[col].append([0,0,0,1]) # out of bounds
                else:
                    #
                    if walls[ col+grid_start[0] ][ row+grid_start[1] ] == True:
                        grid[col].append([0,0,0,1])# wall 
                    elif food[ col+grid_start[0] ][ row+grid_start[1] ] == True:
                        grid[col].append([0,1,0,0])# pellet
                    else:
                        grid[col].append([0,0,1,0])# empty space


        grid[2][2] = '@' #pacman location(always in the middle)

        #add both ghost to grid if position is inside grid range 
        if ghost1[0] < 5 and ghost1[1] < 5 and ghost1[0] > -1 and ghost1[1] > -1:
            grid[int(ghost1[0])][int(ghost1[1])] = [1,0,0,0]
        if ghost2[0] < 5 and ghost2[1] < 5 and ghost2[0] > -1 and ghost2[1] > -1:
            grid[int(ghost2[0])][int(ghost2[1])] = [1,0,0,0]

        #iterates through capsule list and adds if position is inside grid range
        for i in range(0,len(capsules)):
            distance = [capsules[i][0] - grid_start[0], capsules[i][1]-grid_start[1] ]
            if distance[0] < 5 and distance[1] < 5 and distance[0] > -1 and distance[1] > -1:
                grid[distance[0]][distance[1]] = [0,1,0,0]

        input_grid= [] #&&&&
        for col in range(4,-1,-1):
            for row in range(0,5):
                for i in range(0,len(grid[row][col])):
                    input_grid.append(grid[row][col][i])


        del input_grid[len(input_grid)/2] # we don't need the square pacman is in...

        return input_grid


    def getAction(self, state):#pass all game state
        "The agent receives a GameState (defined in pacman.py)."

        # 1.) Get the grid.
        #getGrid returns a 2d array with 24 inputs of
        #1d array to pass as input to ANN
        input_grid = self.getGrid(state)

        # 2.) Input the grid to ANN.
        predictedDirection = self.agentAnn.processInput(input_grid)
        """
        uncomment this section to print direction ea time pacman chooses one
        """
        if predictedDirection == Directions.NORTH:
            print'Direction: North'
        elif predictedDirection == Directions.EAST:
            print'Direction: East'
        elif predictedDirection == Directions.SOUTH:
            print'Direction: South'
        elif predictedDirection == Directions.WEST:
            print'Direction: West'
        else:
            print'Direction unknown!?'

        # 3.) Return the results from ANN.
        if predictedDirection in state.getLegalPacmanActions():
            #return predictedDirection
            return predictedDirection
        else:
            return Directions.STOP


# Agent that turns left wheever it can
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
