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
import random
import util
import math

from game import Agent


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(
            gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(
            len(scores)) if scores[index] == bestScore]
        # Pick randomly among the best
        chosenIndex = random.choice(bestIndices)

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
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
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [
            ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        newFoodPos = newFood.asList()
        newGhostPos = [ghostState.getPosition()
                       for ghostState in newGhostStates]
        ghostScared = any(newScaredTimes)
        if not ghostScared and newPos in newGhostPos:
            return -1
        # Warning:
        # Cannot use `newFood.asList()` here.
        # If there is a food at Pac-Man's new position,
        # `newFood.asList()` will not contain it because it will be eaten.
        # We must use `currentGameState.getFood().asList()` which contains this food.
        elif newPos in currentGameState.getFood().asList():
            return 1
        else:
            minFoodDist = min([util.manhattanDistance(pos, newPos)
                              for pos in newFoodPos])
            minGhostDist = min([util.manhattanDistance(pos, newPos)
                               for pos in newGhostPos])
            return 1 / minFoodDist - 1 / minGhostDist


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()


def searchTerminate(gameState, currDepth, maxDepth):
    """
    Whether the search has ended.
    """
    return currDepth >= maxDepth or gameState.isWin() or gameState.isLose()


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

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """
    _pacman = 0

    def getAction(self, gameState):
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
        self._ghosts = [i for i in range(
            self._pacman + 1, gameState.getNumAgents())]
        assert self._ghosts

        actions = []
        for action in gameState.getLegalActions(self._pacman):
            newState = gameState.generateSuccessor(self._pacman, action)
            actions.append(
                (action, self._getMinimaxValue(newState, self._ghosts[0], 0)))
        return max(actions, key=lambda k: k[1])[0]

    def _getMinimaxValue(self, gameState, agent, currDepth):
        """
        Do a Minimax Search for an agent.
        For Pac-Man, it returns the max value.
        For a ghost, it returns the min value.

        :param gameState: A game state.
        :param agent: An agent, can be Pac-Man or a ghost.
        :param currDepth: The current search depth.
        """
        def minValue(gameState, ghost, currDepth):
            assert ghost != self._pacman
            assert not searchTerminate(gameState, currDepth, self.depth)
            best = math.inf
            for action in gameState.getLegalActions(ghost):
                newState = gameState.generateSuccessor(ghost, action)

                if ghost != self._ghosts[-1]:
                    # All ghosts move in order of increasing index.
                    best = min(best, self._getMinimaxValue(
                        newState, ghost + 1, currDepth))
                else:
                    # It is the last ghost, it's time for Pac-Man in the next round.
                    best = min(best, self._getMinimaxValue(
                        newState, self._pacman, currDepth + 1))
            return best

        def maxValue(gameState, currDepth):
            assert not searchTerminate(gameState, currDepth, self.depth)
            best = -math.inf
            for action in gameState.getLegalActions(self._pacman):
                newState = gameState.generateSuccessor(self._pacman, action)
                best = max(best, self._getMinimaxValue(
                    newState, self._ghosts[0], currDepth))
            return best

        if searchTerminate(gameState, currDepth, self.depth):
            return self.evaluationFunction(gameState)
        else:
            return maxValue(gameState, currDepth) if agent == self._pacman \
                else minValue(gameState, agent, currDepth)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    _pacman = 0

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        self._ghosts = [i for i in range(
            self._pacman + 1, gameState.getNumAgents())]
        assert self._ghosts

        alpha = -math.inf
        bestAction = Directions.STOP
        for action in gameState.getLegalActions(self._pacman):
            newState = gameState.generateSuccessor(self._pacman, action)
            newValue = self._getMinimaxValue(
                newState, self._ghosts[0], 0, alpha, math.inf)
            if newValue > alpha:
                alpha = newValue
                bestAction = action
        return bestAction

    def _getMinimaxValue(self, gameState, agent, currDepth, alpha, beta):
        """
        Do a Minimax Search with Alpha-Beta Pruning for an agent.
        For Pac-Man, it returns the max value.
        For a ghost, it returns the min value.

        :param gameState: A game state.
        :param agent: An agent, can be Pac-Man or a ghost.
        :param currDepth: The current search depth.
        :param alpha: The best (highest-value) choice we have found so far along the path of Maximizers from the current state to the root.
        :param beta: The best (lowest-value) choice we have found so far along the path of Minimizers from the current state to the root.
        """
        def minValue(gameState, ghost, currDepth, alpha, beta):
            assert ghost != self._pacman
            assert not searchTerminate(gameState, currDepth, self.depth)
            best = math.inf
            for action in gameState.getLegalActions(ghost):
                newState = gameState.generateSuccessor(ghost, action)

                if ghost != self._ghosts[-1]:
                    # All ghosts move in order of increasing index.
                    best = min(best, self._getMinimaxValue(
                        newState, ghost + 1, currDepth, alpha, beta))
                else:
                    # It is the last ghost, it's time for Pac-Man in the next round.
                    best = min(best, self._getMinimaxValue(
                        newState, self._pacman, currDepth + 1, alpha, beta))
                if best < alpha:
                    # Return the current minimum value.
                    # It is not a precise value of the current state, just to indicate the value may be worse.
                    # This has been enough for the Maximizer in the upper level.
                    # Because the Maximizer will not select the current state, it already has a better choice.
                    return best
                else:
                    beta = min(beta, best)
            return best

        def maxValue(gameState, currDepth, alpha, beta):
            assert not searchTerminate(gameState, currDepth, self.depth)
            best = -math.inf
            for action in gameState.getLegalActions(self._pacman):
                newState = gameState.generateSuccessor(self._pacman, action)
                best = max(best, self._getMinimaxValue(
                    newState, self._ghosts[0], currDepth, alpha, beta))
                if best > beta:
                    # Return the current maximum value.
                    # It is not a precise value of the current state, just to indicate the value may be worse.
                    # This has been enough for the Minimizer in the upper level.
                    # Because the Minimizer will not select the current state, it already has a better choice.
                    return best
                else:
                    alpha = max(alpha, best)
            return best

        if searchTerminate(gameState, currDepth, self.depth):
            return self.evaluationFunction(gameState)
        else:
            return maxValue(gameState, currDepth, alpha, beta) if agent == self._pacman \
                else minValue(gameState, agent, currDepth, alpha, beta)


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    _pacman = 0

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        self._ghosts = [i for i in range(
            self._pacman + 1, gameState.getNumAgents())]
        assert self._ghosts

        actions = []
        for action in gameState.getLegalActions(self._pacman):
            newState = gameState.generateSuccessor(self._pacman, action)
            actions.append(
                (action, self._getExpectimaxValue(newState, self._ghosts[0], 0)))
        return max(actions, key=lambda k: k[1])[0]

    def _getExpectimaxValue(self, gameState, agent, currDepth):
        """Do an Expectimax Search for an agent.

        :param gameState: A game state.
        :param agent: An agent, can be Pac-Man or a ghost.
        :param currDepth: The current search depth.
        """
        def expValue(gameState, ghost, currDepth):
            assert ghost != self._pacman
            assert not searchTerminate(gameState, currDepth, self.depth)
            score = 0
            actions = gameState.getLegalActions(ghost)
            prob = 1 / len(actions)
            for action in actions:
                newState = gameState.generateSuccessor(ghost, action)

                if ghost != self._ghosts[-1]:
                    # All ghosts move in order of increasing index.
                    score += prob * \
                        self._getExpectimaxValue(
                            newState, ghost + 1, currDepth)
                else:
                    # It is the last ghost, it's time for Pac-Man in the next round.
                    score += prob * \
                        self._getExpectimaxValue(
                            newState, self._pacman, currDepth + 1)
            return score

        def maxValue(gameState, currDepth):
            assert not searchTerminate(gameState, currDepth, self.depth)
            best = -math.inf
            for action in gameState.getLegalActions(self._pacman):
                newState = gameState.generateSuccessor(self._pacman, action)
                best = max(best, self._getExpectimaxValue(
                    newState, self._ghosts[0], currDepth))
            return best

        if searchTerminate(gameState, currDepth, self.depth):
            return self.evaluationFunction(gameState)
        else:
            return maxValue(gameState, currDepth) if agent == self._pacman \
                else expValue(gameState, agent, currDepth)


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviation
better = betterEvaluationFunction
