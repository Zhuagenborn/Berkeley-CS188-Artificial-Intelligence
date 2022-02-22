# analysis.py
# -----------
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


######################
# ANALYSIS QUESTIONS #
######################

# Set the given parameters to obtain the specified policies through
# value iteration.

def question2():
    """
    Make the agent try to cross the bridge.
    """
    answerDiscount = 0.9
    # The agent is not in danger of falling off the bridge.
    answerNoise = 0.0
    return answerDiscount, answerNoise


def question3a():
    """
    Make the agent prefer the close exit, risking the cliff.
    """
    # Walking a long way to the distant exit only gets small rewards.
    answerDiscount = 0.1
    # Not in danger of falling off the cliff.
    answerNoise = 0.0
    # Try to end the game quickly.
    answerLivingReward = -0.1
    return answerDiscount, answerNoise, answerLivingReward


def question3b():
    """
    Make the agent prefer the close exit, avoiding the cliff.
    """
    # Walking a long way to the distant exit only gets small rewards.
    answerDiscount = 0.1
    # In danger of falling off the cliff.
    answerNoise = 0.1
    # Try to end the game quickly.
    answerLivingReward = -0.1
    return answerDiscount, answerNoise, answerLivingReward


def question3c():
    """
    Make the agent prefer the distant exit, risking the cliff.
    """
    # Walking a long way to the distant exit can get large rewards.
    answerDiscount = 0.9
    # Not in danger of falling off the cliff.
    answerNoise = 0
    # Staying alive has no reward.
    answerLivingReward = 0.0
    return answerDiscount, answerNoise, answerLivingReward


def question3d():
    """
    Make the agent prefer the distant exit, avoiding the cliff.
    """
    # Walking a long way to the distant exit can get large rewards.
    answerDiscount = 0.9
    # In danger of falling off the cliff.
    answerNoise = 0.1
    # Staying alive has no reward.
    answerLivingReward = 0
    return answerDiscount, answerNoise, answerLivingReward


def question3e():
    """
    Make the agent avoid both exits and the cliff.
    """
    # Walking a long way to the distant exit only gets small rewards.
    answerDiscount = 0.1
    # In danger of falling off the cliff.
    answerNoise = 0.8
    # Staying alive can be very rewarding.
    answerLivingReward = 2.0
    return answerDiscount, answerNoise, answerLivingReward


def question8():
    answerEpsilon = None
    answerLearningRate = None
    return 'NOT POSSIBLE'


if __name__ == '__main__':
    print('Answers to analysis questions:')
    import analysis
    for q in [q for q in dir(analysis) if q.startswith('question')]:
        response = getattr(analysis, q)()
        print('  Question %s:\t%s' % (q, str(response)))
