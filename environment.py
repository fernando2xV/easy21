#Fernando Victoria easy21

#Description of easy21:
# Infinite deck of cards (cards with replacement)
# Cards are in range [1,10], P[red] = 1/3, P[black] = 2/3
# No aces/picture cards
# At the start --> dealer and player draw 1 black card each (fully observed)
# Each turn the player can a) stick b) hit
# a) Don't receive any further cards
# b) Draw another card from deck
#
# If black card --> ADD
# If red card --> SUB
#
# If player's (sum > 21 || sum < 1) ==> Loses game --> REWARD = -1
#

import random
import copy

class State:
    dealers_card = random.randint(1, 10)
    players_sum = random.randint(1, 10)
    end = 0 #0 -> state hasnt terminated, 1 -> state terminated

def draw_card(deck_sum):
    random_card = random.randint(1, 10)
    dummy = random.random()
    #2/3 of probability --> black --> ADD
    if dummy > 1/3:
        deck_sum = deck_sum + random_card
    else:
        deck_sum = deck_sum - random_card#red --> SUB
    
    return deck_sum

def step(s, a):
#a is 1(hit) or 0(stick)
    if a == 1:
        new_card = draw_card(s.players_sum)
        s.players_sum = s.players_sum + new_card
        if (s.players_sum < 1 or s.players_sum > 21):
            reward = -1
            s.end = 1
            return s, reward
            
        else:
            reward = 0
            s.end = 0
            return s, reward

    elif a == 0:

        while(s.dealers_card < 17):
            s.dealers_card = draw_card(s.dealers_card)

            if (s.dealers_card < 1 or s.dealers_card > 21):
                reward = 1
                s.end = 1
                return s, reward

        if (s.players_sum > s.dealers_card):
            reward = 1
            s.end = 1
            return s, reward

        elif (s. players_sum < s.dealers_card):
            reward = -1
            s.end = 1
            return s, reward

        else:
            reward = 0
            s.end = 1
            return s, reward

