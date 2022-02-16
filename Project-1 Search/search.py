# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util


class SearchNode:
    def __init__(self, state, path=[], cost=0):
        self.state = state
        self.path = path
        self.cost = cost


def totalCost(searchNode, successor, problem=None):
    """Get the total cost from the beginning to a successor.

    :param searchNode: The current search node.
    :param successor: A successor returned by `SearchProblem.getSuccessors`.
    :param problem: The game problem.
    """
    stepCost = successor[2]
    return searchNode.cost + stepCost


def search(problem, containerType, gFunc=None, hFunc=None):
    """Find a path to the destination.

    :param problem: The game problem.
    :param containerType: A node container type, can be `util.Stack`, `util.Queue` or `util.PriorityQueue`.
    :param gFunc: A callback with three parameter: the current search node, a successor and the game problem.
    :param hFunc: A heuristic callback with two parameter: a state and the game problem.
    """
    container = containerType()
    if containerType == util.PriorityQueue:
        assert(gFunc)
        container.push(SearchNode(problem.getStartState()), 0)
    else:
        container.push(SearchNode(problem.getStartState()))

    visited = set()
    while not container.isEmpty():
        node = container.pop()
        if node.state in visited:
            continue
        elif problem.isGoalState(node.state):
            return node.path

        visited.add(node.state)
        for successor in problem.getSuccessors(node.state):
            newState, dir, stepCost = successor
            if newState not in visited:
                if containerType == util.PriorityQueue:
                    heuristic = gFunc(node, successor, problem)
                    if hFunc:
                        heuristic += hFunc(newState, problem)
                    container.push(
                        SearchNode(newState, node.path + [dir], node.cost + stepCost), heuristic)
                else:
                    container.push(SearchNode(newState, node.path + [dir]))
    return []


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    return search(problem, util.Stack)


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    return search(problem, util.Queue)


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    return search(problem, util.PriorityQueue, totalCost)


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    return search(problem, util.PriorityQueue, totalCost, heuristic)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
