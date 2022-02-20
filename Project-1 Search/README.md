# Search

![Cover](images/Cover.png)

## Introduction

In this project, your *Pac-Man* agent will find paths through his maze world, both to reach a particular location and to collect food efficiently. You will build general search algorithms and apply them to *Pac-Man* scenarios.

This project includes an autograder for you to grade your answers on your machine. This can be run with the command:

```bash
python autograder.py
```

The code for this project consists of several *Python* files, some of which you will need to read and understand in order to complete the assignment, and some of which you can ignore.

**Files you'll edit:**

|       File        |                    Description                     |
| :---------------: | :------------------------------------------------: |
|    `search.py`    |  Where all of your search algorithms will reside.  |
| `searchAgents.py` | Where all of your search-based agents will reside. |

**Files you might want to look at:**

|    File     |                                                                   Description                                                                    |
| :---------: | :----------------------------------------------------------------------------------------------------------------------------------------------: |
| `pacman.py` |            The main file that runs *Pac-Man* games. This file describes a *Pac-Man* `GameState` type, which you use in this project.             |
|  `game.py`  | The logic behind how *Pac-Man* world works. This file describes several supporting types like `AgentState`, `Agent`, `Direction` and `Grid`. |
|  `util.py`  |                                            Useful data structures for implementing search algorithms.                                            |

**Supporting files you can ignore:**

|          File          |                        Description                         |
| :--------------------: | :--------------------------------------------------------: |
|  `graphicsDisplay.py`  |                  Graphics for *Pac-Man*.                   |
|   `graphicsUtils.py`   |              Support for *Pac-Man* graphics.               |
|    `textDisplay.py`    |               ASCII graphics for *Pac-Man*.                |
|    `ghostAgents.py`    |                 Agents to control ghosts.                  |
|  `keyboardAgents.py`   |         Keyboard interfaces to control *Pac-Man*.          |
|      `layout.py`       | Code for reading layout files and storing their contents.  |
|    `autograder.py`     |                    Project autograder.                     |
|    `testParser.py`     |         Parses autograder test and solution files.         |
|    `testClasses.py`    |             General autograding test classes.              |
|     `test_cases/`      |   Directory containing the test cases for each question.   |
| `searchTestClasses.py` | Specific autograding test classes for this project. |

## Welcome to Pac-Man

You should be able to play a game of *Pac-Man* by typing the following at the command line:

```bash
python pacman.py
```

The simplest agent in `searchAgents.py` is called `GoWestAgent`, which always goes west (a trivial reflex agent). This agent can occasionally win:

```bash
python pacman.py --layout testMaze --pacman GoWestAgent
```

But, things get ugly for this agent when turning is required:

```bash
python pacman.py --layout tinyMaze --pacman GoWestAgent
```

If *Pac-Man* gets stuck, you can exit the game by typing <kbd>Ctrl</kbd> + <kbd>C</kbd> into your terminal.

Soon, your agent will solve not only `tinyMaze`, but any maze you want.

Note that `pacman.py` supports a number of options that can each be expressed in a long way (e.g., `--layout`) or a short way (e.g., `-l`). You can see the list of all options and their default values via:

```bash
python pacman.py -h
```

Also, all of the commands that appear in this project also appear in `commands.txt`.

## Question 1 - Finding a Fixed Food Dot using Depth-First Search

In `searchAgents.py`, you'll find a fully implemented `SearchAgent`, which plans out a path through *Pac-Man*'s world and then executes that path step-by-step. The search algorithms for formulating a plan are not implemented – that's your job.

First, test that `SearchAgent` is working correctly by running:

```bash
python pacman.py -l tinyMaze -p SearchAgent -a fn=tinyMazeSearch
```

The command above tells `SearchAgent` to use `tinyMazeSearch` as its search algorithm, which is implemented in `search.py`. *Pac-Man* should navigate the maze successfully.

Now it's time to write full-fledged generic search functions to help *Pac-Man* plan routes! Remember that a search node must contain not only a state but also the information necessary to reconstruct the path (plan) which gets to that state.

**Important Notes:**

- All of your search functions need to return a list of actions that will lead the agent from the start to the goal. These actions all have to be legal moves (valid directions, no moving through walls).
- Make sure to use `Stack`, `Queue` and `PriorityQueue` data structures provided to you in `util.py`! These data structure implementations have particular properties which are required for compatibility with the autograder.

Implement *Depth-First Search (DFS)* algorithm in `depthFirstSearch` function in `search.py`. To make your algorithm complete, write a graph search version, which avoids expanding any already visited states.

Your code should quickly find a solution for:

```bash
python pacman.py -l tinyMaze -p SearchAgent
```

```bash
python pacman.py -l mediumMaze -p SearchAgent
```

```bash
python pacman.py -l bigMaze -z .5 -p SearchAgent
```

The *Pac-Man* board will show an overlay of the states explored, and the order in which they were explored (brighter red means earlier exploration).

## Question 2 - Breadth-First Search

Implement *Breadth-First Search (BFS)* algorithm in `breadthFirstSearch` function in `search.py`. Again, write a graph search algorithm that avoids expanding any already visited states. Test your code the same way you did for *Depth-First Search*.

```bash
python pacman.py -l mediumMaze -p SearchAgent -a fn=bfs
```

```bash
python pacman.py -l bigMaze -p SearchAgent -a fn=bfs -z .5
```

If *Pac-Man* moves too slowly for you, try the option `--frameTime 0`.

## Question 3 - Varying the Cost Function

While *Breadth-First Search* will find a fewest-actions path to the goal, we might want to find paths that are "best" in other senses. Consider `mediumDottedMaze` and `mediumScaryMaze`.

By changing the cost function, we can encourage *Pac-Man* to find different paths. For example, we can charge more for dangerous steps in ghost-ridden areas or less for steps in food-rich areas, and a rational *Pac-Man* agent should adjust its behavior in response.

Implement *Uniform-Cost Search (UCS)* algorithm in `uniformCostSearch` function in `search.py`. We encourage you to look through `util.py` for some data structures that may be useful in your implementation. You should now observe successful behavior in all three of the following layouts, where the agents below are all *UCS* agents that differ only in the cost function they use (the agents and cost functions are written for you):

```bash
python pacman.py -l mediumMaze -p SearchAgent -a fn=ucs
```

```bash
python pacman.py -l mediumDottedMaze -p StayEastSearchAgent
```

```bash
python pacman.py -l mediumScaryMaze -p StayWestSearchAgent
```

You should get very low and very high path costs for `StayEastSearchAgent` and `StayWestSearchAgent` respectively, due to their exponential cost functions (see `searchAgents.py` for details).

## Question 4 - A\* Search

Implement *A\* Search* in empty function `aStarSearch` in `search.py`. *A\** takes a heuristic function as an argument. Heuristics take two arguments: a state in the search problem (the main argument), and the problem itself (for reference information). `nullHeuristic` in `search.py` is a trivial example.

You can test your *A\** implementation on the original problem of finding a path through a maze to a fixed position using the *Manhattan* distance heuristic (implemented already as `manhattanHeuristic` in `searchAgents.py`).

```bash
python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic
```

You should see that *A\** finds the optimal solution slightly faster than *Uniform-Cost Search*.

## Question 5 - Finding All the Corners

The real power of *A\** will only be apparent with a more challenging search problem. Now, it's time to formulate a new problem and design a heuristic for it.

In corner mazes, there are four dots, one in each corner. Our new search problem is to find the shortest path through the maze that touches all four corners (whether the maze actually has food there or not). Note that for some mazes like `tinyCorners`, the shortest path does not always go to the closest food first!

Implement `CornersProblem` search problem in `searchAgents.py`. You will need to choose a state representation that encodes all the information necessary to detect whether all four corners have been reached. Now, your search agent should solve:

```bash
python pacman.py -l tinyCorners -p SearchAgent -a fn=bfs,prob=CornersProblem
```

```bash
python pacman.py -l mediumCorners -p SearchAgent -a fn=bfs,prob=CornersProblem
```

To receive full credit, you need to define an abstract state representation that does not encode irrelevant information (like the position of ghosts, where extra food is, etc.). In particular, do not use a *Pac-Man* `GameState` as a search state. Your code will be very, very slow if you do (and also wrong).

**Hint:** The only parts of the game state you need to reference in your implementation are the starting *Pac-Man* position and the location of the four corners.

## Question 6 - Corners Problem: Heuristic

Implement a non-trivial, consistent heuristic for `CornersProblem` in `cornersHeuristic`.

```bash
python pacman.py -l mediumCorners -p AStarCornersAgent -z 0.5
```

Note that `AStarCornersAgent` is a shortcut for

```bash
-p SearchAgent -a fn=aStarSearch,prob=CornersProblem,heuristic=cornersHeuristic
```

**Admissibility vs. Consistency:** Remember, heuristics are just functions that take search states and return numbers that estimate the cost to a nearest goal. More effective heuristics will return values closer to the actual goal costs. To be admissible, the heuristic values must be lower bounds on the actual shortest path cost to the nearest goal (and non-negative). To be consistent, it must additionally hold that if an action has cost $c$, then taking that action can only cause a drop in heuristic of at most $c$.

**Non-Trivial Heuristics:** The trivial heuristics are the ones that return zero everywhere (*UCS*) and the heuristic which computes the true completion cost. The former won't save you any time, while the latter will timeout the autograder. You want a heuristic which reduces total compute time.

**Grading:** Your heuristic must be a non-trivial non-negative consistent heuristic to receive any points. Make sure that your heuristic returns zero at every goal state and never returns a negative value.

## Question 7 - Eating All The Dots

Now we'll solve a hard search problem: eating all the *Pac-Man* food in as few steps as possible. For this, we'll need a new search problem definition which formalizes the food-clearing problem: `FoodSearchProblem` in `searchAgents.py` (implemented for you). A solution is defined to be a path that collects all of the food in the *Pac-Man* world. For the present project, solutions do not take into account any ghosts or power pellets; solutions only depend on the placement of walls, regular food and *Pac-Man*. If you have written your general search methods correctly, *A\** with a null heuristic (equivalent to *Uniform-Cost Search*) should quickly find an optimal solution to `testSearch`.

```bash
python pacman.py -l testSearch -p AStarFoodSearchAgent
```

Note that `AStarFoodSearchAgent` is a shortcut for

```bash
-p SearchAgent -a fn=astar,prob=FoodSearchProblem,heuristic=foodHeuristic
```

Fill in `foodHeuristic` in `searchAgents.py` with a consistent heuristic for `FoodSearchProblem`. Try your agent on `trickySearch` board:

```bash
python pacman.py -l trickySearch -p AStarFoodSearchAgent
```

## Question 8 - Suboptimal Search

Sometimes, even with *A\** and a good heuristic, finding the optimal path through all the dots is hard. In these cases, we'd still like to find a reasonably good path, quickly. In this section, you'll write an agent that always greedily eats the closest dot. `ClosestDotSearchAgent` is implemented for you in `searchAgents.py`, but it's missing a key function that finds a path to the closest dot.

Implement function `findPathToClosestDot` in `searchAgents.py`.

```bash
python pacman.py -l bigSearch -p ClosestDotSearchAgent -z .5
```

**Hint:** The quickest way to complete `findPathToClosestDot` is to fill in `AnyFoodSearchProblem`, which is missing its goal test. Then, solve that problem with an appropriate search function. The solution should be very short! And `ClosestDotSearchAgent` won't always find the shortest possible path through the maze. Make sure you understand why and try to come up with a small example where repeatedly going to the closest dot does not result in finding the shortest path for eating all the dots.