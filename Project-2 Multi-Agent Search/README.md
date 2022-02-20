# Multi-Agent Search

![Cover](images/Cover.png)

## Introduction

In this project, you will design agents for the classic version of *Pac-Man*, including ghosts. Along the way, you will implement both *Minimax Search* and *Expectimax Search* and try your hand at evaluation function design.

This project includes an autograder for you to grade your answers on your machine. This can be run with the command:

```bash
python autograder.py
```

By default, the autograder displays graphics with the `-t` option, but doesn't with the `-q` option. You can force graphics by using the `--graphics` flag, or force no graphics by using the `--no-graphics` flag.

The code for this project consists of several *Python* files, some of which you will need to read and understand in order to complete the assignment, and some of which you can ignore.

**Files you'll edit:**

|       File       |                       Description                        |
| :--------------: | :------------------------------------------------------: |
| `multiAgents.py` | Where all of your multi-agent search agents will reside. |

**Files you might want to look at:**

|    File     |                                                                 Description                                                                  |
| :---------: | :------------------------------------------------------------------------------------------------------------------------------------------: |
| `pacman.py` |          The main file that runs *Pac-Man* games. This file describes a *Pac-Man* `GameState` type, which you use in this project.           |
|  `game.py`  | The logic behind how *Pac-Man* world works. This file describes several supporting types like `AgentState`, `Agent`, `Direction` and `Grid`. |
|  `util.py`  |                                          Useful data structures for implementing search algorithms.                                          |

**Supporting files you can ignore:**

|            File            |                        Description                        |
| :------------------------: | :-------------------------------------------------------: |
|    `graphicsDisplay.py`    |                  Graphics for *Pac-Man*.                  |
|     `graphicsUtils.py`     |              Support for *Pac-Man* graphics.              |
|      `textDisplay.py`      |               ASCII graphics for *Pac-Man*.               |
|      `ghostAgents.py`      |                 Agents to control ghosts.                 |
|    `keyboardAgents.py`     |         Keyboard interfaces to control *Pac-Man*.         |
|        `layout.py`         | Code for reading layout files and storing their contents. |
|      `autograder.py`       |                    Project autograder.                    |
|      `testParser.py`       |        Parses autograder test and solution files.         |
|      `testClasses.py`      |             General autograding test classes.             |
|       `test_cases/`        |  Directory containing the test cases for each question.   |
| `multiagentTestClasses.py` |    Specific autograding test classes for this project.    |

## Welcome to Multi-Agent Pac-Man

First, play a game of classic *Pac-Man* by running the following command:

```bash
python pacman.py
```

and using the arrow keys to move. Now, run the provided `ReflexAgent` in `multiAgents.py`

```bash
python pacman.py -p ReflexAgent
```

Note that it plays quite poorly even on simple layouts:

```bash
python pacman.py -p ReflexAgent -l testClassic
```

Inspect its code in `multiAgents.py` and make sure you understand what it's doing.

## Question 1 - Reflex Agent

Improve `ReflexAgent` in `multiAgents.py` to play respectably. The provided reflex agent code provides some helpful examples of methods that query `GameState` for information. A capable reflex agent will have to consider both food locations and ghost locations to perform well. Your agent should easily and reliably clear `testClassic` layout:

```bash
python pacman.py -p ReflexAgent -l testClassic
```

Try out your reflex agent on default `mediumClassic` layout with one ghost or two (and animation off to speed up the display):

```bash
python pacman.py --frameTime 0 -p ReflexAgent -k 1
```

```bash
python pacman.py --frameTime 0 -p ReflexAgent -k 2
```

How does your agent fare? It will likely often die with two ghosts on the default board, unless your evaluation function is quite good.

**Notes:**

- Remember that `newFood` has function `asList()`.
- As features, try the reciprocal of important values (such as distance to food) rather than just the values themselves.
- The evaluation function you're writing is evaluating state-action pairs; in later parts of the project, you'll be evaluating states.
- You may find it useful to view the internal contents of various objects for debugging. You can do this by printing the objects' string representations. For example, you can print `newGhostStates` with `print(newGhostStates)`.

Default ghosts are random; you can also play for fun with slightly smarter directional ghosts using `-g DirectionalGhost`. If the randomness is preventing you from telling whether your agent is improving, you can use `-f` to run with a fixed random seed (same random choices every game). You can also play multiple games in a row with `-n`. Turn off graphics with `-q` to run lots of games quickly.

You can try your agent out under these conditions with

```bash
python autograder.py -q q1
```

To run it without graphics, use

```bash
python autograder.py -q q1 --no-graphics
```

## Question 2 - Minimax

Now you will write an adversarial search agent in provided `MinimaxAgent` class stub in `multiAgents.py`. Your *Minimax* agent should work with any number of ghosts, so you'll have to write an algorithm that is slightly more general than what you've previously seen in lecture. In particular, your *Minimax Tree* will have multiple min layers (one for each ghost) for every max layer.

Your code should also expand the game tree to an arbitrary depth. Score the leaves of your *Minimax Tree* with supplied `self.evaluationFunction`, which defaults to `scoreEvaluationFunction`. `MinimaxAgent` extends `MultiAgentSearchAgent`, which gives access to `self.depth` and `self.evaluationFunction`. Make sure your *Minimax* code makes reference to these two variables where appropriate as these variables are populated in response to command line options.

Note that a single search ply is considered to be one *Pac-Man* move and all the ghosts' responses, so depth-two search will involve *Pac-Man* and each ghost moving two times.

**Notes:**

- Implement the algorithm recursively using helper functions.

- The correct implementation of *Minimax* will lead to *Pac-Man* losing the game in some tests. This is not a problem: as it is correct behaviour, it will pass the tests.

- The evaluation function for *Pac-Man* test in this part is already written (`self.evaluationFunction`). You shouldn't change this function, but recognize that now we're evaluating states rather than actions, as we were for the reflex agent. Look-ahead agents evaluate future states whereas reflex agents evaluate actions from the current state.

- *Pac-Man* is always agent *0*, and the agents move in order of increasing agent index.

- All states in *Minimax* should be `GameStates`, either passed in to `getAction` or generated via `GameState.generateSuccessor`. In this project, you will not be abstracting to simplified states.

- On larger boards such as `openClassic` and `mediumClassic` (the default), you'll find *Pac-Man* to be good at not dying, but quite bad at winning. He'll often thrash around without making progress. He might even thrash around right next to a dot without eating it because he doesn't know where he'd go after eating that dot. Don't worry if you see this behavior. *Question 5* will clean up all of these issues.

- When *Pac-Man* believes that his death is unavoidable, he will try to end the game as soon as possible because of the constant penalty for living. Sometimes, this is the wrong thing to do with random ghosts, but *Minimax* agents always assume the worst:

  ```bash
  python pacman.py -p MinimaxAgent -l trappedClassic -a depth=3
  ```

  Make sure you understand why *Pac-Man* rushes the closest ghost in this case.

To test and debug your code, run

```bash
python autograder.py -q q2
```

This will show what your algorithm does on a number of small trees, as well as a *Pac-Man* game. To run it without graphics, use

```bash
python autograder.py -q q2 --no-graphics
```

## Question 3 - Alpha-Beta Pruning

Make a new agent that uses *Alpha-Beta Pruning* to more efficiently explore the *Minimax Tree*, in `AlphaBetaAgent`. Again, your algorithm will be slightly more general than the pseudocode from lecture, so part of the challenge is to extend the *Alpha-Beta Pruning* logic appropriately to multiple minimizer agents.

You should see a speed-up.

```bash
python pacman.py -p AlphaBetaAgent -a depth=3 -l smallClassic
```

The `AlphaBetaAgent` *Minimax* values should be identical to the `MinimaxAgent` *Minimax* values, although the actions it selects can vary because of different tie-breaking behavior.

The pseudo-code below represents the algorithm you should implement for this question.

![Alpha-Beta-Pseudo](images/Alpha-Beta-Pseudo.png)

To test and debug your code, run

```bash
python autograder.py -q q3
```

This will show what your algorithm does on a number of small trees, as well as a *Pac-Man* game. To run it without graphics, use

```bash
python autograder.py -q q3 --no-graphics
```

The correct implementation of *Alpha-Beta Pruning* will lead to *Pac-Man* losing some of the tests. This is not a problem: as it is correct behaviour, it will pass the tests.

## Question 4 - Expectimax

*Minimax* and *Alpha-Beta Pruning* are great, but they both assume that you are playing against an adversary who makes optimal decisions. As anyone who has ever won *Tic-Tac-Toe* can tell you, this is not always the case. In this question you will implement `ExpectimaxAgent`, which is useful for modeling probabilistic behavior of agents who may make suboptimal choices.

To expedite your own development, we've supplied some test cases based on generic trees. You can debug your implementation on small the game trees using the command:

```bash
python autograder.py -q q4
```

Once your algorithm is working on small trees, you can observe its success in *Pac-Man*. Random ghosts are of course not optimal *Minimax* agents, and so modeling them with *Minimax Search* may not be appropriate. `ExpectimaxAgent`, will no longer take the min over all ghost actions, but the expectation according to your agent's model of how the ghosts act. To simplify your code, assume you will only be running against an adversary which chooses amongst their `getLegalActions` uniformly at random.

To see how `ExpectimaxAgent` behaves in *Pac-Man*, run

```bash
python pacman.py -p ExpectimaxAgent -l minimaxClassic -a depth=3
```

You should now observe a more cavalier approach in close quarters with ghosts. In particular, if *Pac-Man* perceives that he could be trapped but might escape to grab a few more pieces of food, he'll at least try. Investigate the results of these two scenarios:

```bash
python pacman.py -p AlphaBetaAgent -l trappedClassic -a depth=3 -q -n 10
```

```bash
python pacman.py -p ExpectimaxAgent -l trappedClassic -a depth=3 -q -n 10
```

You should find that your `ExpectimaxAgent` wins about half the time, while your `AlphaBetaAgent` always loses. Make sure you understand why the behavior here differs from the *Minimax* case.

The correct implementation of *Expectimax* will lead to *Pac-Man* losing some of the tests. This is not a problem: as it is correct behaviour, it will pass the tests.

## Question 5 - Evaluation Function

Write a better evaluation function for *Pac-Man* in provided function `betterEvaluationFunction`. The evaluation function should evaluate states, rather than actions like your reflex agent evaluation function did. With depth-two search, your evaluation function should clear `smallClassic` layout with a random ghost more than half the time and still run at a reasonable rate.

You can try your agent out under these conditions with

```bash
python autograder.py -q q5
```

To run it without graphics, use

```bash
python autograder.py -q q5 --no-graphics
```