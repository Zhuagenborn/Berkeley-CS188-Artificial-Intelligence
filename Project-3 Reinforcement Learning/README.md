# Reinforcement Learning

## Introduction

In this project, you will implement *Value Iteration* and *Q-Learning*. You will test your agents first on grid worlds, then apply them to a simulated robot controller crawler and *Pac-Man*.

This project includes an autograder for you to grade your answers on your machine. This can be run with the command:

```bash
python autograder.py
```

The code for this project consists of several *Python* files, some of which you will need to read and understand in order to complete the assignment, and some of which you can ignore.

**Files you'll edit:**

|           File            |                              Description                               |
| :-----------------------: | :--------------------------------------------------------------------: |
| `valueIterationAgents.py` | A *Value Iteration* agent for solving known *Markov Decision Process*. |
|   `qlearningAgents.py`    |    *Q-Learning* agents for grid worlds, the crawler and *Pac-Man*.     |
|       `analysis.py`       |     A file to put your answers to questions given in the project.      |

**Files you might want to look at:**

|          File          |                                                          Description                                                           |
| :--------------------: | :----------------------------------------------------------------------------------------------------------------------------: |
|        `mdp.py`        |                                     Defines methods on general *Markov Decision Process*.                                      |
|  `learningAgents.py`   |              Defines the base classes `ValueEstimationAgent` and `QLearningAgent`, which your agents will extend.              |
|       `util.py`        |                      Utilities, including `util.Counter`, which is particularly useful for *Q-Learning*.                       |
|     `gridworld.py`     |                                                 The grid world implementation.                                                 |
| `featureExtractors.py` | Classes for extracting features on pairs of state and action. Used for *Approximate Q-Learning* agent in `qlearningAgents.py`. |

**Supporting files you can ignore:**

|             File              |                                        Description                                        |
| :---------------------------: | :---------------------------------------------------------------------------------------: |
|       `environment.py`        | Abstract class for general *Reinforcement Learning* environments. Used by `gridworld.py`. |
| `graphicsGridworldDisplay.py` |                                 Graphics for grid worlds.                                 |
|      `graphicsUtils.py`       |                                    Graphics utilities.                                    |
|   `textGridworldDisplay.py`   |                              ASCII graphics for grid worlds.                              |
|         `crawler.py`          |                            The crawler code and test harness.                             |
|  `graphicsCrawlerDisplay.py`  |                              Graphics for the crawler robot.                              |
|        `autograder.py`        |                                    Project autograder.                                    |
|        `testParser.py`        |                        Parses autograder test and solution files.                         |
|       `testClasses.py`        |                             General autograding test classes.                             |
|         `test_cases/`         |                  Directory containing the test cases for each question.                   |
| `reinforcementTestClasses.py` |                    Specific autograding test classes for this project.                    |

## Markov Decision Process

To get started, run a grid world in manual control mode, which uses the arrow keys.

```bash
python gridworld.py -m
```

You will see the two-exit layout from class. The blue dot is the agent. Note that when you press up, the agent only actually moves north *80%* of the time. Such is the life of a grid world agent!

You can control many aspects of the simulation. A full list of options is available by running

```bash
python gridworld.py -h
```

The default agent moves randomly.

```bash
python gridworld.py -g MazeGrid
```

You should see the random agent bounce around the grid until it happens upon an exit. Not the finest hour for an AI agent.

Note that *Markov Decision Process (MDP)* of grid worlds is such that you first must enter a pre-terminal state (the double boxes shown in the graphics) and then take the special exit action before the episode actually ends (in the true terminal state called `TERMINAL_STATE`, which is not shown in the graphics). If you run an episode manually, your total return may be less than you expected, due to the discount rate (`-d` to change; *0.9* by default).

Look at the console output that accompanies the graphical output (or use `-t` for all text). You will be told about each transition the agent experiences (to turn this off, use `-q`). By default, most transitions will receive a reward of zero, though you can change this with the living reward option `-r`.

## Question 1 - Value Iteration

Recall *Value Iteration* state update equation:

$$
V_{k + 1}(s) \leftarrow \max_{a} \sum_{s'} T(s, a, s') \biggl[R(s, a, s') + \gamma V_{k}(s') \biggr]
$$

Write a *Value Iteration* agent in `ValueIterationAgent`, which has been partially specified for you in `valueIterationAgents.py`. Your agent is an offline planner, not a *Reinforcement Learning* agent, and so the relevant training option is the number of iterations it should run (option `-i`) in its initial planning phase. `ValueIterationAgent` takes an *MDP* on construction and runs *Value Iteration* for the specified number of iterations before the constructor returns.

*Value Iteration* computes $k$-step estimates of the optimal values, $V_{k}$. In addition to running *Value Iteration*, implement the following methods for `ValueIterationAgent` using $V_{k}$.

- `computeActionFromValues(state)` computes the best action according to the value function given by `self.values`.
- `computeQValueFromValues(state, action)` returns *Q-Value* of `(state, action)` pair given by the value function given by `self.values`.

These quantities are all displayed in the graphics: values are numbers in squares, *Q-Value* are numbers in square quarters, and policies are arrows out from each square.

**Notes:**

- Use the batch version of *Value Iteration* where each vector $V_{k}$ is computed from a fixed vector $V_{k - 1}$, not the online version where one single weight vector is updated in place. This means that when a state's value is updated in iteration $k$ based on the values of its successor states, the successor state values used in the value update computation should be those from iteration $k - 1$ (even if some of the successor states had already been updated in iteration $k$).
- A policy synthesized from values of depth $k$ (which reflect the next $k$ rewards) will actually reflect the next $k + 1$ rewards (i.e. you return $\pi_{k - 1}$). Similarly, *Q-Values* will also reflect one more reward than the values (i.e. you return $Q_{k + 1}$). You should return the synthesized policy $\pi_{k + 1}$.
- You may optionally use `util.Counter` class in `util.py`, which is a dictionary with a default value of zero. However, be careful with `argMax`: the actual *Argmax* you want may be a key not in the counter!
- Make sure to handle the case when a state has no available actions in an *MDP* (think about what this means for future rewards).

To test your implementation, run the autograder.

```bash
python autograder.py -q q1
```

The following command loads your `ValueIterationAgent`, which will compute a policy and execute it *10* times. Press a key to cycle through values, *Q-Values*, and the simulation. You should find that the value of the start state (`V(start)`, which you can read off of the graphics) and the empirical resulting average reward (printed after the *10* rounds of execution finish) are quite close.

```bash
python gridworld.py -a value -i 100 -k 10
```

On default `BookGrid`, running *Value Iteration* for *5* iterations should give you this output:

```bash
python gridworld.py -a value -i 5
```

![Q1-5-Iteration-Values](images/Q1-5-Iteration-Values.png)

## Question 2 - Bridge Crossing Analysis

`BridgeGrid` is a grid world map with the a low-reward terminal state and a high-reward terminal state separated by a narrow bridge, on either side of which is a chasm of high negative reward. The agent starts near the low-reward state. With the default discount of *0.9* and the default noise of *0.2*, the optimal policy does not cross the bridge. Change only one of the discount and noise parameters in `question2()` of `analysis.py` so that the optimal policy causes the agent to attempt to cross the bridge. Noise refers to how often an agent ends up in an unintended successor state when they perform an action. The default corresponds to:

```bash
python gridworld.py -a value -i 100 -g BridgeGrid --discount 0.9 --noise 0.2
```

![Q2-100-Iteration-Values](images/Q2-100-Iteration-Values.png)

To test your implementation, run the autograder.

```bash
python autograder.py -q q2
```

## Question 3 - Policies

Consider `DiscountGrid` layout, shown below. This grid has two terminal states with positive payoff (in the middle row), a close exit with payoff *+1* and a distant exit with payoff *+10*. The bottom row of the grid consists of terminal states with negative payoff (shown in red); each state in this cliff region has payoff *-10*. The starting state is the yellow square. We distinguish between two types of paths:

- Paths that risk the cliff and travel near the bottom row of the grid; these paths are shorter but risk earning a large negative payoff, and are represented by the red arrow in the figure below.
- Paths that avoid the cliff and travel along the top edge of the grid. These paths are longer but are less likely to incur huge negative payoffs. These paths are represented by the green arrow in the figure below.

![Q3-Cliff-Paths](images/Q3-Cliff-Paths.png)

In this question, you will choose settings of the discount, noise, and living reward parameters for this *MDP* to produce optimal policies of several different types. Your setting of the parameter values for each part should have the property that, if your agent followed its optimal policy without being subject to any noise, it would exhibit the given behavior. If a particular behavior is not achieved for any setting of the parameters, assert that the policy is impossible by returning the string `NOT POSSIBLE`.

Here are the optimal policy types you should attempt to produce:

- Prefer the close exit (*+1*), risking the cliff (*-10*).
- Prefer the close exit (*+1*), but avoiding the cliff (*-10*).
- Prefer the distant exit (*+10*), risking the cliff (*-10*).
- Prefer the distant exit (*+10*), avoiding the cliff (*-10*).
- Avoid both exits and the cliff (so an episode should never terminate).

To test your implementation, run the autograder.

```bash
python autograder.py -q q3
```

`question3a()` through `question3e()` should each return a three-item tuple of discount, noise and living reward in `analysis.py`.

## Question 4 - Asynchronous Value Iteration

Write a *Value Iteration* agent in `AsynchronousValueIterationAgent`, which has been partially specified for you in `valueIterationAgents.py`. Your agent is an offline planner, not a *Reinforcement Learning* agent, and so the relevant training option is the number of iterations it should run (option `-i`) in its initial planning phase. `AsynchronousValueIterationAgent` takes an *MDP* on construction and runs *Cyclic Value Iteration* for the specified number of iterations before the constructor returns. Note that all this iteration code should be placed inside the constructor (`__init__` method).

The reason this class is called `AsynchronousValueIterationAgent` is because we will update only one state in each iteration, as opposed to doing a batch-style update. Here is how *Cyclic Value Iteration* works. In the first iteration, only update the value of the first state in the states list. In the second iteration, only update the value of the second. Keep going until you have updated the value of each state once, then start back at the first state for the subsequent iteration. If the state picked for updating is terminal, nothing happens in that iteration. You can implement it as indexing into the states variable defined in the code skeleton.

*Value Iteration* iterates a fixed-point equation. It is also possible to update the state values in different ways, such as in a random order (i.e., select a state randomly, update its value, and repeat) or in a batch style. In this question, we will explore another technique.

`AsynchronousValueIterationAgent` inherits from `ValueIterationAgent`, so the only method you need to implement is `runValueIteration`. Since the superclass constructor calls `runValueIteration`, overriding it is sufficient to change the agent's behavior as desired.

Make sure to handle the case when a state has no available actions in an *MDP* (think about what this means for future rewards).

To test your implementation, run the autograder. It should take less than a second to run. If it takes much longer, you may run into issues later in the project, so make your implementation more efficient now.

```bash
python autograder.py -q q4
```

The following command loads your `AsynchronousValueIterationAgent` in a grid world, which will compute a policy and execute it *10* times. Press a key to cycle through values, *Q-Values*, and the simulation. You should find that the value of the start state (`V(start)`, which you can read off of the graphics) and the empirical resulting average reward (printed after the *10* rounds of execution finish) are quite close.

```bash
python gridworld.py -a asynchvalue -i 1000 -k 10
```

## Question 5 - Prioritized Sweeping Value Iteration

You will now implement `PrioritizedSweepingValueIterationAgent`, which has been partially specified for you in `valueIterationAgents.py`. Note that this class derives from `AsynchronousValueIterationAgent`, so the only method that needs to change is `runValueIteration`, which actually runs the *Value Iteration*.

*Prioritized Sweeping* attempts to focus updates of state values in ways that are likely to change the policy.

For this project, you will implement a simplified version of the standard *Prioritized Sweeping* algorithm. We've adapted this algorithm for our setting. First, we define the predecessors of a state `s` as all states that have a nonzero probability of reaching `s` by taking some action `a`. Also, `theta`, which is passed in as a parameter, will represent our tolerance for error when deciding whether to update the value of a state. Here's the algorithm you should follow in your implementation.

- Compute predecessors of all states.
- Initialize an empty priority queue.
- For each non-terminal state `s`, do: (note: to make the autograder work for this question, you must iterate over states in the order returned by `self.mdp.getStates()`)

  - Find the absolute value of the difference between the current value of `s` in `self.values` and the highest *Q-Value* across all possible actions from `s` (this represents what the value should be); call this number `diff`. Do not update `self.values[s]` in this step.
  - Push `s` into the priority queue with priority `-diff` (note that this is negative). We use a negative because the priority queue is a min heap, but we want to prioritize updating states that have a higher error.

- For `iteration` in `0, 1, 2, ..., self.iterations - 1`, do:

  - If the priority queue is empty, then terminate.
  - Pop a state `s` off the priority queue.
  - Update the value of `s` (if it is not a terminal state) in `self.values`.
  - For each predecessor `p` of `s`, do:

    - Find the absolute value of the difference between the current value of `p` in `self.values` and the highest *Q-Value* across all possible actions from `p` (this represents what the value should be); call this number `diff`. Do not update `self.values[p]` in this step.
    - If `diff` ＞ `theta`, push `p` into the priority queue with priority `-diff` (note that this is negative), as long as it does not already exist in the priority queue with equal or lower priority. As before, we use a negative because the priority queue is a min heap, but we want to prioritize updating states that have a higher error.

A couple of important notes on implementation:

- When you compute predecessors of a state, make sure to store them in a set, not a list, to avoid duplicates.
- Please use `util.PriorityQueue` in your implementation. The `update` method in this class will likely be useful; look at its documentation.

To test your implementation, run the autograder.

```bash
python autograder.py -q q5
```

You can run `PrioritizedSweepingValueIterationAgen` in a grid world using the following command.

```bash
python gridworld.py -a priosweepvalue -i 1000
```

## Question 6 - Q-Learning

Note that your *Value Iteration* agent does not actually learn from experience. Rather, it ponders its *MDP* model to arrive at a complete policy before ever interacting with a real environment. When it does interact with the environment, it simply follows the precomputed policy (e.g. it becomes a reflex agent). This distinction may be subtle in a simulated environment like a grid world, but it's very important in the real world, where the real *MDP* is not available.

You will now write a *Q-Learning* agent, which does very little on construction, but instead learns by trial and error from interactions with the environment through its `update(state, action, nextState, reward)` method. A stub of a *Q-Learner* is specified in `QLearningAgent` in `qlearningAgents.py`, and you can select it with the option `-a q`. For this question, you must implement `update`, `computeValueFromQValues`, `getQValue`, and `computeActionFromQValues` methods.

**Notes:**

- For `computeActionFromQValues`, you should break ties randomly for better behavior. `random.choice()` will help. In a particular state, actions that your agent hasn't seen before still have a *Q-Value*, specifically zero, and if all of the actions that your agent has seen before have a negative *Q-Value*, an unseen action may be optimal.
- Make sure that in your `computeValueFromQValues` and `computeActionFromQValues` methods, you only access *Q-Values* by calling `getQValue`.

With *Q-Learning* update in place, you can watch your *Q-Learner* learn under manual control, using the keyboard:

```bash
python gridworld.py -a q -k 5 -m
```

Recall that `-k` will control the number of episodes your agent gets to learn. Watch how the agent learns about the state it was just in, not the one it moves to, and leaves learning in its wake. To help with debugging, you can turn off noise by using `--noise 0.0`.

## Question 7 - Epsilon-Greedy

Complete your *Q-Learning* agent by implementing *Epsilon-Greedy* action selection in `getAction`, meaning it chooses random actions an epsilon fraction of the time, and follows its current best *Q-Values* otherwise. Note that choosing a random action may result in choosing the best action - that is, you should not choose a random sub-optimal action, but rather any random legal action.

You can choose an element from a list uniformly at random by calling `random.choice`. You can simulate a binary variable with probability `p` of success by using `util.flipCoin(p)`, which returns `True` with probability `p` and `False` with probability `1 - p`.

After implementing `getAction`, observe the following behavior of the agent in a grid world with epsilon *0.3*.

```bash
python gridworld.py -a q -k 100
```

Your final *Q-Values* should resemble those of your *Value Iteration* agent, especially along well-traveled paths. However, your average returns will be lower than the *Q-Values* predict because of the random actions and the initial learning phase.

You can also observe the following simulations for different epsilon values. Does that behavior of the agent match what you expect?

```bash
python gridworld.py -a q -k 100 --noise 0.0 -e 0.1
```

```bash
python gridworld.py -a q -k 100 --noise 0.0 -e 0.9
```

To test your implementation, run the autograder.

```bash
python autograder.py -q q7
```

With no additional code, you should now be able to run a *Q-Learning* crawler robot.

```bash
python crawler.py
```

If this doesn't work, you've probably written some code too specific to `GridWorld` problem and you should make it more general to all *MDPs*.

This will invoke the crawler robot using your *Q-Learner*. Play around with the various learning parameters to see how they affect the agent's policies and actions. Note that the step delay is a parameter of the simulation, whereas the learning rate and epsilon are parameters of your learning algorithm, and the discount factor is a property of the environment.

## Question 8 - Bridge Crossing Revisited

First, train a completely random *Q-Learner* with the default learning rate on noiseless `BridgeGrid` for *50* episodes and observe whether it finds the optimal policy.

```bash
python gridworld.py -a q -k 50 -n 0 -g BridgeGrid -e 1
```

Now try the same experiment with an epsilon of *0*. Is there an epsilon and a learning rate for which it is highly likely (greater than *99%*) that the optimal policy will be learned after *50* iterations? `question8()` in `analysis.py` should return either a two-item tuple of epsilon, learning rate or the string `NOT POSSIBLE` if there is none. Epsilon is controlled by `-e`, learning rate by `-l`.

Note that your response should be not depend on the exact tie-breaking mechanism used to choose actions. This means your answer should be correct even if for instance we rotated the entire bridge grid world *90* degrees.

To test your implementation, run the autograder.

```bash
python autograder.py -q q8
```

## Question 9 - Q-Learning and Pac-Man

Time to play some *Pac-Man*! *Pac-Man* will play games in two phases. In the first phase, training, *Pac-Man* will begin to learn about the values of positions and actions. Because it takes a very long time to learn accurate *Q-Values* even for tiny grids, *Pac-Man*'s training games run in quiet mode by default, with no graphics (or console) display. Once *Pac-Man*'s training is complete, he will enter testing mode. When testing, *Pac-Man*'s `self.epsilon` and `self.alpha` will be set to *0.0*, effectively stopping *Q-Learning* and disabling exploration, in order to allow *Pac-Man* to exploit his learned policy. Test games are shown in the graphics by default. Without any code changes you should be able to run *Q-Learning* *Pac-Man* for very tiny grids as follows:

```bash
python pacman.py -p PacmanQAgent -x 2000 -n 2010 -l smallGrid
```

Note that `PacmanQAgent` is already defined for you in terms of the `QLearningAgent` you've already written. `PacmanQAgent` is only different in that it has default learning parameters that are more effective for *Pac-Man* problem (`epsilon=0.05, alpha=0.2, gamma=0.8`). You will receive full credit for this question if the command above works without exceptions and your agent wins at least *80%* of the time. The autograder will run *100* test games after the *2000* training games.

**Notes:**

- If your `QLearningAgent` works for `gridworld.py` and `crawler.py` but does not seem to be learning a good policy for *Pac-Man* on `smallGrid`, it may be because your `getAction` or `computeActionFromQValues` methods do not in some cases properly consider unseen actions. In particular, because unseen actions have by definition a *Q-Value* of zero, if all of the actions that have been seen have negative *Q-Values*, an unseen action may be optimal. Beware of `argMax` function from `util.Counter`!

- If you want to experiment with learning parameters, you can use the option `-a`, for example `-a epsilon=0.1,alpha=0.3,gamma=0.7`. These values will then be accessible as `self.epsilon`, `self.gamma` and `self.alpha` inside the agent.

- While a total of *2010* games will be played, the first *2000* games will not be displayed because of the option `-x 2000`, which designates the first *2000* games for training (no output). Thus, you will only see *Pac-Man* play the last *10* of these games. The number of training games is also passed to your agent as the option `numTraining`. If you want to watch *10* training games to see what's going on, use the command

  ```bash
  python pacman.py -p PacmanQAgent -n 10 -l smallGrid -a numTraining=10
  ```

To test your implementation, run the autograder.

```bash
python autograder.py -q q9
```

During training, you will see output every *100* games with statistics about how *Pac-Man* is faring. Epsilon is positive during training, so *Pac-Man* will play poorly even after having learned a good policy: this is because he occasionally makes a random exploratory move into a ghost. As a benchmark, it should take between *1000* and *1400* games before *Pac-Man*'s rewards for a *100* episode segment becomes positive, reflecting that he's started winning more than losing. By the end of training, it should remain positive and be fairly high (between *100* and *350*).

Make sure you understand what is happening here: the *MDP* state is the exact board configuration facing *Pac-Man*, with the now complex transitions describing an entire ply of change to that state. The intermediate game configurations in which *Pac-Man* has moved but the ghosts have not replied are not *MDP* states, but are bundled in to the transitions.

Once *Pac-Man* is done training, he should win very reliably in test games (at least *90%* of the time), since now he is exploiting his learned policy.

However, you will find that training the same agent on seemingly simple `mediumGrid` does not work well. In our implementation, *Pac-Man*'s average training rewards remain negative throughout training. At test time, he plays badly, probably losing all of his test games. Training will also take a long time, despite its ineffectiveness.

*Pac-Man* fails to win on larger layouts because each board configuration is a separate state with separate *Q-Values*. He has no way to generalize that running into a ghost is bad for all positions. Obviously, this approach will not scale.

## Question 10 - Approximate Q-Learning

Implement an *Approximate Q-Learning* agent that learns weights for features of states, where many states might share the same features. Write your implementation in `ApproximateQAgent` class in `qlearningAgents.py`, which is a subclass of `PacmanQAgent`.

Note that *Approximate Q-Learning* assumes the existence of a feature function $f(s, a)$ over state and action pairs, which yields a vector $\bigl[f_{1}(s, a),\, \ldots,\, f_{i}(s, a),\, \ldots,\, f_{n}(s, a) \bigr]$ of feature values. We provide feature functions for you in `featureExtractors.py`. Feature vectors are `util.Counter` (like a dictionary) objects containing the non-zero pairs of features and values; all omitted features have value zero.

*Approximate Q-function* takes the following form:

$$
Q(s, a) = \sum_{i = 1}^{n} f_{i}(s, a) \cdot w_{i}
$$

where each weight $w_{i}$ is associated with a particular feature $f_{i}(s, a)$. In your code, you should implement the weight vector as a dictionary mapping features (which the feature extractors will return) to weight values. You will update your weight vectors similarly to how you updated *Q-Values*:

$$
w_{i} \leftarrow w_{i} + \alpha \cdot \text{difference} \cdot f_{i}(s, a)
$$

$$
\text{difference} = \bigl(r + \gamma \max_{a'} Q(s', a') \bigr) - Q(s, a)
$$

Note that $\text{difference}$ term is the same as in normal *Q-Learning*, and $r$ is the experienced reward.

By default, `ApproximateQAgent` uses `IdentityExtractor`, which assigns a single feature to every `(state, action)` pair. With this feature extractor, your *Approximate Q-Learning* agent should work identically to `PacmanQAgent`. You can test this with the following command:

```bash
python pacman.py -p ApproximateQAgent -x 2000 -n 2010 -l smallGrid
```

Note that `ApproximateQAgent` is a subclass of `QLearningAgent`, and it therefore shares several methods like `getAction`. Make sure that your methods in `QLearningAgent` call `getQValue` instead of accessing *Q-Values* directly, so that when you override `getQValue` in your approximate agent, the new approximate *Q-Values* are used to compute actions.

Once you're confident that your approximate learner works correctly with the identity features, run your *Approximate Q-Learning* agent with our custom feature extractor, which can learn to win with ease:

```bash
python pacman.py -p ApproximateQAgent -a extractor=SimpleExtractor -x 50 -n 60 -l mediumGrid
```

Even much larger layouts should be no problem for your `ApproximateQAgent`.

```bash
python pacman.py -p ApproximateQAgent -a extractor=SimpleExtractor -x 50 -n 60 -l mediumClassic
```

If you have no errors, your agent should win almost every time with these simple features, even with only *50* training games.

To test your implementation, run the autograder.

```bash
python autograder.py -q q10
```