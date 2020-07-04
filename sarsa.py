
import environment
import random
from environment import *
from montecarlo import *
import numpy as np
import math
import copy

#sarsa with eligibility traces

def sarsa(q,counter,lambda_var):
    state = State()
    state.dealers_card = random.randint(1,10)
    state.players_sum = random.randint(1,10)

    E = np.zeros((2,11,22))

    while state.end == 0:

        e = 100 / (100 + np.sum(counter[:,state.dealers_card, state.players_sum],axis=0))
        action = epsilon_greedy(q, state, e)

        E[action, state.dealers_card, state.players_sum] += 1

        old_dealercard = state.dealers_card
        old_playersum = state.players_sum

        q_old = q[action, old_dealercard, old_playersum]
        counter[action, old_dealercard, old_playersum] += 1

        old_state = copy.copy(state)

        state, reward = step(state, action)

        e = 100 / (100 + np.sum(counter[:,old_dealercard, old_playersum],axis=0))
        action_prime = epsilon_greedy(q, old_state, e)


        if state.end == 1:
            td_error = reward - q_old
        else:
            #td_error += np.amax(value[:,state.dealers_card,state.players_sum],axis=0)
            td_error = reward + q[action_prime, state.dealers_card, state.players_sum] - q_old

        alpha = 1 / counter[action, old_dealercard, old_playersum]
        q[action, old_dealercard, old_playersum] = q[action, old_dealercard, old_playersum] + alpha * td_error * E[action, old_dealercard, old_playersum]

        E = E * lambda_var


    return q, counter