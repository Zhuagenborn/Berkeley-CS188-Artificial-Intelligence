# Ghostbusters

![Cover](images/Cover.png)

## Introduction

*Pac-Man* spends his life running from ghosts, but things were not always so. Legend has it that many years ago, *Pac-Man*'s great grandfather *Grand-Pac* learned to hunt ghosts for sport. However, he was blinded by his power and could only track ghosts by their banging and clanging.

In this project, you will design *Pac-Man* agents that use sensors to locate and eat invisible ghosts. You'll advance from locating single, stationary ghosts to hunting packs of multiple moving ghosts with ruthless efficiency.

The code for this project consists of several *Python* files, some of which you will need to read and understand in order to complete the assignment, and some of which you can ignore.

**Files you'll edit:**

|        File        |                       Description                       |
| :----------------: | :-----------------------------------------------------: |
| `bustersAgents.py` | Agents for playing *Ghostbusters* variant of *Pac-Man*. |
|   `inference.py`   | Code for tracking ghosts over time using their sounds.  |

**Files you might want to look at:**

|          File           |                   Description                    |
| :---------------------: | :----------------------------------------------: |
|      `busters.py`       |        The main entry to *Ghostbusters*.         |
| `bustersGhostAgents.py` |       New ghost agents for *Ghostbusters*.       |
| `distanceCalculator.py` |             Computes maze distances.             |
|        `game.py`        | Inner workings and helper classes for *Pac-Man*. |
|    `ghostAgents.py`     |            Agents to control ghosts.             |

**Supporting files you can ignore:**

|         File         |                        Description                        |
| :------------------: | :-------------------------------------------------------: |
| `graphicsDisplay.py` |                  Graphics for *Pac-Man*.                  |
|  `graphicsUtils.py`  |                    Graphics utilities.                    |
| `keyboardAgents.py`  |         Keyboard interfaces to control *Pac-Man*.         |
|     `layout.py`      | Code for reading layout files and storing their contents. |
|   `autograder.py`    |                    Project autograder.                    |
|   `testParser.py`    |        Parses autograder test and solution files.         |
|   `testClasses.py`   |             General autograding test classes.             |
|    `test_cases/`     |  Directory containing the test cases for each question.   |
|      `util.py`       |                    Utility functions.                     |

## Ghostbusters & Bayes Networks

In *Ghostbusters*, the goal is to hunt down scared but invisible ghosts. *Pac-Man*, ever resourceful, is equipped with sonar (ears) that provides noisy readings of the *Manhattan* distance to each ghost. The game ends when *Pac-Man* has eaten all the ghosts. To start, try playing a game yourself using the keyboard.

```bash
python busters.py
```

The blocks of color indicate where the each ghost could possibly be, given the noisy distance readings provided to *Pac-Man*. The noisy distances at the bottom of the display are always non-negative, and always within 7 of the true distance. The probability of a distance reading decreases exponentially with its difference from the true distance.

Your primary task in this project is to implement inference to track the ghosts. For the keyboard based game above, a crude form of inference was implemented for you by default: all squares in which a ghost could possibly be are shaded by the color of the ghost. Naturally, we want a better estimate of the ghost's position. Fortunately, *Bayes Networks* provide us with powerful tools for making the most of the information we have. Throughout the rest of this project, you will implement algorithms for performing both exact and approximate inference using *Bayes Networks*.

While watching and debugging your code with the autograder, it will be helpful to have some understanding of what the autograder is doing. There are two types of tests in this project, as differentiated by their `.test` files found in the subdirectories of `test_cases` folder. For tests of class `DoubleInferenceAgentTest`, you will see visualizations of the inference distributions generated by your code, but all *Pac-Man* actions will be pre-selected according to the actions of the staff implementation. This is necessary to allow comparision of your distributions with the staff's distributions. The second type of test is `GameScoreTest`, in which your `BustersAgent` will actually select actions for *Pac-Man* and you will watch your *Pac-Man* play and win games.

As you implement and debug your code, you may find it useful to run a single test at a time. In order to do this you will need to use the `-t` flag with the autograder. For example if you only want to run the first test of *Question 1*, use

```bash
python autograder.py -t test_cases/q1/1-ObsProb
```

In general, all test cases can be found inside `test_cases/q*`.

For this project, it is possible sometimes for the autograder to time out if running the tests with graphics. To accurately determine whether or not your code is efficient enough, you should run the tests with the `--no-graphics` flag.

## Question 0 - Discrete Distribution

Throughout this project, we will be using `DiscreteDistribution` class defined in `inference.py` to model belief distributions and weight distributions. This class is an extension of the built-in *Python* dictionary class, where the keys are the different discrete elements of our distribution, and the corresponding values are proportional to the belief or weight that the distribution assigns that element. This question asks you to fill in the missing parts of this class, which will be crucial for later questions.

First, fill in `normalize` method, which normalizes the values in the distribution to sum to one, but keeps the proportions of the values the same. Use `total` method to find the sum of the values in the distribution. For an empty distribution or a distribution where all of the values are zero, do nothing. Note that this method modifies the distribution directly, rather than returning a new distribution.

Second, fill in `sample` method, which draws a sample from the distribution, where the probability that a key is sampled is proportional to its corresponding value. Assume that the distribution is not empty, and not all of the values are zero. Note that the distribution does not necessarily have to be normalized prior to calling this method. You may find *Python*'s built-in `random.random()` function useful for this question.

There are no autograder tests for this question, but the correctness of your implementation can be easily checked. We have provided *Python* `doctests` as a starting point, and you can feel free to add more and implement other tests of your own. You can run `doctests` using

```bash
python -m doctest -v inference.py
```

Note that, depending on the implementation details of `sample` method, some correct implementations may not pass `doctests` that are provided. To thoroughly check the correctness of your `sample` method, you should instead draw many samples and see if the frequency of each key converges to be proportional of its corresponding value.

## Question 1 - Observation Probability

In this question, you will implement `getObservationProb` method in `InferenceModule` base class in `inference.py`. This method takes in an observation (which is a noisy reading of the distance to the ghost), *Pac-Man*'s position, the ghost's position, and the position of the ghost's jail, and returns the probability of the noisy distance reading given *Pac-Man*'s position and the ghost's position. In other words, we want to return `P(noisyDistance | pacmanPosition, ghostPosition)`.

The distance sensor has a probability distribution over distance readings given the true distance from *Pac-Man* to the ghost. This distribution is modeled by function `busters.getObservationProbability(noisyDistance, trueDistance)`, which returns `P(noisyDistance | trueDistance)` and is provided for you. You should use this function to help you solve the problem, and use the provided `manhattanDistance` function to find the distance between *Pac-Man*'s location and the ghost's location.

However, there is the special case of jail that we have to handle as well. Specifically, when we capture a ghost and send it to the jail location, our distance sensor deterministically returns `None`, and nothing else. So, if the ghost's position is the jail position, then the observation is `None` with probability one, and everything else with probability zero. Conversely, if the distance reading is not `None`, then the ghost is in jail with probability zero. If the distance reading is `None` then the ghost is in jail with probability one. Make sure you handle this special case in your implementation.

To test your code and run the autograder for this question:

```bash
python autograder.py -q q1
```

## Question 2 - Exact Inference Observation

In this question, you will implement `observeUpdate` method in `ExactInference` class of `inference.py` to correctly update the agent's belief distribution over ghost positions given an observation from *Pac-Man*'s sensors. You are implementing the online belief update for observing new evidence. `observeUpdate` method should, for this problem, update the belief at every position on the map after receiving a sensor reading. You should iterate your updates over variable `self.allPositions` which includes all legal positions plus the special jail position. Beliefs represent the probability that the ghost is at a particular location, and are stored as a `DiscreteDistribution` object in a field called `self.beliefs`, which you should update.

Before typing any code, write down the equation of the inference problem you are trying to solve. You should use function `self.getObservationProb` that you wrote in the last question, which returns the probability of an observation given *Pac-Man*'s position, a potential ghost position, and the jail position. You can obtain *Pac-Man*'s position using `gameState.getPacmanPosition()`, and the jail position using `self.getJailPosition()`.

In *Pac-Man* display, high posterior beliefs are represented by bright colors, while low beliefs are represented by dim colors. You should start with a large cloud of belief that shrinks over time as more evidence accumulates. As you watch the test cases, be sure that you understand how the squares converge to their final coloring.

Note that your busters agents have a separate inference module for each ghost they are tracking. That's why if you print an observation inside `observeUpdate` function, you'll only see a single number even though there may be multiple ghosts on the board.

To run the autograder for this question and visualize the output:

```bash
python autograder.py -q q2
```

## Question 3 - Exact Inference with Time Elapse

In the previous question you implemented belief updates for *Pac-Man* based on his observations. Fortunately, *Pac-Man*'s observations are not his only source of knowledge about where a ghost may be. *Pac-Man* also has knowledge about the ways that a ghost may move; namely that the ghost can not move through a wall or more than one space in one time step.

To understand why this is useful to *Pac-Man*, consider the following scenario in which there is *Pac-Man* and one ghost. *Pac-Man* receives many observations which indicate the ghost is very near, but then one which indicates the ghost is very far. The reading indicating the ghost is very far is likely to be the result of a buggy sensor. *Pac-Man*'s prior knowledge of how the ghost may move will decrease the impact of this reading since *Pac-Man* knows the ghost could not move so far in only one move.

In this question, you will implement `elapseTime` method in `ExactInference`. `elapseTime` step should, for this problem, update the belief at every position on the map after one time step elapsing. Your agent has access to the action distribution for the ghost through `self.getPositionDistribution`. In order to obtain the distribution over new positions for the ghost, given its previous position, use this line of code:

```python
newPosDist = self.getPositionDistribution(gameState, oldPos)
```

Where `oldPos` refers to the previous ghost position. `newPosDist` is a `DiscreteDistribution` object, where for each position `p` in `self.allPositions`, `newPosDist[p]` is the probability that the ghost is at position `p` at time `t + 1`, given that the ghost is at position `oldPos` at time `t`. Note that this call can be fairly expensive, so if your code is timing out, one thing to think about is whether or not you can reduce the number of calls to `self.getPositionDistribution`.

Before typing any code, write down the equation of the inference problem you are trying to solve. In order to test your predict implementation separately from your update implementation in the previous question, this question will not make use of your update implementation.

Since *Pac-Man* is not observing the ghost, this means the ghost's actions will not impact *Pac-Man*'s beliefs. Over time, *Pac-Man*'s beliefs will come to reflect places on the board where he believes ghosts are most likely to be given the geometry of the board and what *Pac-Man* already knows about their valid movements.

For the tests in this question we will sometimes use a ghost with random movements and other times we will use `GoSouthGhost`. This ghost tends to move south so over time, and without any observations, *Pac-Man*'s belief distribution should begin to focus around the bottom of the board. To see which ghost is used for each test case you can look in `.test` files.

To run the autograder for this question and visualize the output:

```bash
python autograder.py -q q3
```

As you watch the autograder output, remember that lighter squares indicate that *Pac-Man* believes a ghost is more likely to occupy that location, and darker squares indicate a ghost is less likely to occupy that location. For which of the test cases do you notice differences emerging in the shading of the squares? Can you explain why some squares get lighter and some squares get darker?

## Question 4 - Exact Inference Full Test

Now that *Pac-Man* knows how to use both his prior knowledge and his observations when figuring out where a ghost is, he is ready to hunt down ghosts on his own. This question will use your `observeUpdate` and `elapseTime` implementations together, along with a simple greedy hunting strategy which you will implement for this question. In the simple greedy strategy, *Pac-Man* assumes that each ghost is in its most likely position according to his beliefs, then moves toward the closest ghost. Up to this point, *Pac-Man* has moved by randomly selecting a valid action.

Implement `chooseAction` method in `GreedyBustersAgent` in `bustersAgents.py`. Your agent should first find the most likely position of each remaining uncaptured ghost, then choose an action that minimizes the maze distance to the closest ghost.

To find the maze distance between any two positions `pos1` and `pos2`, use `self.distancer.getDistance(pos1, pos2)`. To find the successor position of a position after an action:

```python
successorPosition = Actions.getSuccessor(position, action)
```

You are provided with `livingGhostPositionDistributions`, a list of `DiscreteDistribution` objects representing the position belief distributions for each of the ghosts that are still uncaptured.

If correctly implemented, your agent should win the game in `q4/3-gameScoreTest` with a score greater than *700* at least *8* out of *10* times.

To run the autograder for this question and visualize the output:

```bash
python autograder.py -q q4
```

## Question 5 - Approximate Inference Initialization and Beliefs

Approximate inference is very trendy among ghost hunters this season. For the next few questions, you will implement a particle filtering algorithm for tracking a single ghost.

First, implement `initializeUniformly` and `getBeliefDistribution` methods in `ParticleFilter` class in `inference.py`. A particle (sample) is a ghost position in this inference problem. Note that, for initialization, particles should be evenly (not randomly) distributed across legal positions in order to ensure a uniform prior.

Note that the variable you store your particles in must be a list. A list is simply a collection of unweighted variables (positions in this case). Storing your particles as any other data type, such as a dictionary, is incorrect and will produce errors. `getBeliefDistribution` method then takes the list of particles and converts it into a `DiscreteDistribution` object.

To test your code and run the autograder for this question:

```bash
python autograder.py -q q5
```

## Question 6 - Approximate Inference Observation

Next, we will implement `observeUpdate` method in `ParticleFilter` class in `inference.py`. This method constructs a weight distribution over `self.particles` where the weight of a particle is the probability of the observation given *Pac-Man*'s position and that particle location. Then, we resample from this weighted distribution to construct our new list of particles.

You should again use the function `self.getObservationProb` to find the probability of an observation given *Pac-Man*'s position, a potential ghost position, and the jail position. The sample method of `DiscreteDistribution` class will also be useful. As a reminder, you can obtain *Pac-Man*'s position using `gameState.getPacmanPosition()`, and the jail position using `self.getJailPosition()`.

There is one special case that a correct implementation must handle. When all particles receive zero weight, the list of particles should be reinitialized by calling `initializeUniformly`. The total method of `DiscreteDistribution` may be useful.

To run the autograder for this question and visualize the output:

```bash
python autograder.py -q q6
```

## Question 7 - Approximate Inference with Time Elapse

Implement `elapseTime` function in `ParticleFilter` class in `inference.py`. This function should construct a new list of particles that corresponds to each existing particle in self.particles advancing a time step, and then assign this new list back to `self.particles`. When complete, you should be able to track ghosts nearly as effectively as with exact inference.

Note that in this question, we will test both `elapseTime` function in isolation, as well as the full implementation of the particle filter combining `elapseTime` and `observe`.

As in `elapseTime` method of `ExactInference` class, you should use:

```python
newPosDist = self.getPositionDistribution(gameState, oldPos)
```

This line of code obtains the distribution over new positions for the ghost, given its previous position (`oldPos`). The sample method of `DiscreteDistribution` class will also be useful.

To run the autograder for this question and visualize the output:

```bash
python autograder.py -q q7
```

## Question 8 - Joint Particle Filter Observation (1)

So far, we have tracked each ghost independently, which works fine for default `RandomGhost` or more advanced `DirectionalGhost`. However, the prized `DispersingGhost` chooses actions that avoid other ghosts. Since the ghosts' transition models are no longer independent, all ghosts must be tracked jointly in a dynamic *Bayes Network*!

The *Bayes Network* has the following structure, where the hidden variables `G` represent ghost positions and the emission variables `E` are the noisy distances to each ghost. This structure can be extended to more ghosts, but only two (`a` and `b`) are shown below.

![Bayes-Network](images/Bayes-Network.png)

You will now implement a particle filter that tracks multiple ghosts simultaneously. Each particle will represent a tuple of ghost positions that is a sample of where all the ghosts are at the present time. The code is already set up to extract marginal distributions about each ghost from the joint inference algorithm you will create, so that belief clouds about individual ghosts can be displayed.

Complete `initializeUniformly` method in `JointParticleFilter` in `inference.py`. Your initialization should be consistent with a uniform prior. You may find the *Python* `itertools` package helpful. However, note that, if you use this, the permutations are not returned in a random order. Therefore, you must then shuffle the list of permutations in order to ensure even placement of particles across the board.

As before, use `self.legalPositions` to obtain a list of positions a ghost may occupy. Also as before, the variable you store your particles in must be a list.

To run the autograder for this question and visualize the output:

```bash
python autograder.py -q q8
```

## Question 9 - Joint Particle Filter Observation (2)

In this question, you will complete `observeUpdate` method in the `JointParticleFilter` class of `inference.py`. A correct implementation will weight and resample the entire list of particles based on the observation of all ghost distances.

To loop over all the ghosts, use:

```python
for i in range(self.numGhosts):
    pass
```

You can still obtain *Pac-Man*'s position using `gameState.getPacmanPosition()`, but to get the jail position for a ghost, use `self.getJailPosition(i)`, since now there are multiple ghosts each with their own jail positions.

Your implementation should also again handle the special case when all particles receive zero weight. In this case, `self.particles` should be recreated from the prior distribution by calling `initializeUniformly`.

As in `observeUpdate` method for `ParticleFilter` class, you should again use `self.getObservationProb` to find the probability of an observation given *Pac-Man*'s position, a potential ghost position, and the jail position. The sample method of `DiscreteDistribution` class will also be useful.

To run the autograder for this question and visualize the output:

```bash
python autograder.py -q q9
```

## Question 10 - Joint Particle Filter Time Elapse and Full Test

Complete `elapseTime` method in `JointParticleFilter` in `inference.py` to resample each particle correctly for *Bayes Networks*. In particular, each ghost should draw a new position conditioned on the positions of all the ghosts at the previous time step.

As in the last question, you can loop over the ghosts using:

```python
for i in range(self.numGhosts):
    pass
```

Then, assuming that `i` refers to the index of the ghost, to obtain the distributions over new positions for that single ghost, given the list (`prevGhostPositions`) of previous positions of all of the ghosts, use:

```python
newPosDist = self.getPositionDistribution(gameState, prevGhostPositions, i, self.ghostAgents[i])
```

To run the autograder for this question and visualize the output:

```bash
python autograder.py -q q10
```