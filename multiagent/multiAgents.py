# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood().asList()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        distanceToGhost = [manhattanDistance(newPos, ghostState.getPosition()) for ghostState in newGhostStates]
        distanceToFood = [manhattanDistance(newPos, food) for food in newFood]
        
        if len(newFood) == 0:
            if min(distanceToGhost) != 0:
                return float('inf')
            # If there's ghost on the last food, then don't eat
            return -float('inf')
        return min(distanceToGhost) /  min(distanceToFood) ** 1.3 + 2 * successorGameState.getScore()

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        maxVal = -float('inf')
        for action in gameState.getLegalActions(0): # Pacman is always agent 0
            nextState = gameState.generateSuccessor(0, action=action)
            value = self.getValue(nextState, 1, 0)
            if value > maxVal:
                maxVal = value
                bestAction = action
        return bestAction

    def getValue(self, gameState, agentIndex, depth):
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState)
        if agentIndex == 0:
            depth += 1
            if depth == self.depth:
                return self.evaluationFunction(gameState)
            return self.max_value(gameState, depth)
        return self.min_value(gameState, agentIndex, depth)

    def max_value(self, gameState, depth):
        maxVal = -float('inf')
        for action in gameState.getLegalActions(0): # Pacman is always agent 0
            nextState = gameState.generateSuccessor(0, action=action)
            value = self.getValue(nextState, 1, depth)
            if value > maxVal:
                maxVal = value
        return maxVal

    def min_value(self, gameState, agentIndex, depth):
        minVal = float('inf')
        legalActions = gameState.getLegalActions(agentIndex)
        for action in legalActions:
            nextState = gameState.generateSuccessor(agentIndex, action=action)
            value = self.getValue(nextState, (agentIndex + 1) % gameState.getNumAgents(), depth)
            if value < minVal:
                minVal = value
        return minVal

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        maxVal = -float('inf')
        alpha = -float('inf') # MAX's best option on path to root
        beta = float('inf') # MIN's best option on path to root
        for action in gameState.getLegalActions(0): # Pacman is always agent 0
            nextState = gameState.generateSuccessor(0, action=action)
            value = self.minimax(nextState, 1, 0, alpha, beta)
            if value > maxVal:
                maxVal = value
                bestAction = action
            alpha = max(alpha, value)
        return bestAction
    
    def minimax(self, gameState, agentIndex, depth, alpha, beta):
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState)
        if agentIndex == 0:
            depth += 1
            if depth == self.depth:
                return self.evaluationFunction(gameState)
            return self.max_value(gameState, depth, alpha, beta)
        return self.min_value(gameState, agentIndex, depth, alpha, beta)

    def max_value(self, gameState, depth, alpha, beta):
        maxVal = -float('inf')
        for action in gameState.getLegalActions(0): # Pacman is always agent 0
            nextState = gameState.generateSuccessor(0, action=action)
            value = self.minimax(nextState, 1, depth, alpha, beta)
            if value > beta:
                return value
            if value > maxVal:
                maxVal = value
            alpha = max(alpha, value)
        return maxVal

    def min_value(self, gameState, agentIndex, depth, alpha, beta):
        minVal = float('inf')
        legalActions = gameState.getLegalActions(agentIndex)
        for action in legalActions:
            nextState = gameState.generateSuccessor(agentIndex, action=action)
            value = self.minimax(nextState, (agentIndex + 1) % gameState.getNumAgents(), depth, alpha, beta)
            if value < alpha: 
                return value
            if value < minVal:
                minVal = value
            beta = min(beta, value)
        return minVal

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        maxVal = -float('inf')
        for action in gameState.getLegalActions(0): # Pacman is always agent 0
            nextState = gameState.generateSuccessor(0, action=action)
            value = self.expectimax(nextState, 1, 0)
            if value > maxVal:
                maxVal = value
                bestAction = action
        return bestAction
    
    def expectimax(self, gameState, agentIndex, depth):
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState)
        if agentIndex == 0:
            depth += 1
            if depth == self.depth:
                return self.evaluationFunction(gameState)
            return self.maxValue(gameState, depth)
        return self.expValue(gameState, agentIndex, depth)

    def maxValue(self, gameState, depth):
        maxVal = -float('inf')
        for action in gameState.getLegalActions(0): # Pacman is always agent 0
            nextState = gameState.generateSuccessor(0, action=action)
            value = self.expectimax(nextState, 1, depth)
            if value > maxVal:
                maxVal = value
        return maxVal

    def expValue(self, gameState, agentIndex, depth):
        value = 0
        legalActions = gameState.getLegalActions(agentIndex)
        for action in legalActions:
            nextState = gameState.generateSuccessor(agentIndex, action=action)
            value += self.expectimax(nextState, (agentIndex + 1) % gameState.getNumAgents(), depth)

        return value / len(legalActions)

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    pos = currentGameState.getPacmanPosition()
    curFood = currentGameState.getFood().asList()
    ghostStates = currentGameState.getGhostStates()

    distanceToGhost = [manhattanDistance(pos, ghostState.getPosition()) for ghostState in ghostStates]
    distanceToFood = [manhattanDistance(pos, food) for food in curFood]

    # If return a fixed value, all path would have same val,
    # Pacman would don't konw where to go
    if len(curFood) == 0:
        return currentGameState.getScore()
    return min(distanceToGhost) /  min(distanceToFood) ** 1.3 + 2 * currentGameState.getScore()


# Abbreviation
better = betterEvaluationFunction
