
import environment
import random
from environment import *
import numpy as np


#Incremental Monte-Carlo updates (lecture 4)
#	V(St) --> V(St) + alpha(Gt - V(St))

#policy
def epsilon_greedy(v,state,  e):
	#explore
	if(random.random() < e):
		action = random.randint(0, 1)
	#exploit
	else:
		action = np.argmax(v[:, state.dealers_card, state.players_sum])
	return action

#change v for q, as it takes actions and states
def montecarlo(v, counter):
	state = State()
	state.dealers_card = random.randint(1, 10)
	state.players_sum = random.randint(1, 10)
	reward_total = 0
	visits = []#this will be used to store 1x3 matrices containing action taken, dealers sum and players sum
	N0 = 100
	while state.end != 1:
		action = None
		e = N0 / (N0 + np.sum(counter[:, state.dealers_card, state.players_sum], axis = 0))

		#explore/exploit
		action = epsilon_greedy(v,state, e)

		#N(a, St) --> N(a, St) + 1
		counter[action, state.dealers_card, state.players_sum] = counter[action, state.dealers_card, state.players_sum] + 1

		visits.append((action, state.dealers_card, state.players_sum))			
		state, reward = step(state, action)
		reward_total = reward_total + reward

	for action, dealers_card, players_sum in visits:
		G = reward_total

		#alpha = 1/N(a, St)
		alpha = 1 / (counter[action, dealers_card, players_sum])

		#q(a,St) <-- q(a, St) + 1/N(a, St)(Gt - q(a, St))
		v[action, dealers_card, players_sum] = v[action, dealers_card, players_sum] + alpha * (G - v[action, dealers_card, players_sum])

	return v, counter

