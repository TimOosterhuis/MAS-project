SUITS = ['Hearts', 'Spades', 'Diamonds', 'Clubs']

NORMAL_POINTS = {'nine' : 2,
                 'jack' : 7,
                 'ten' : 10,
                 'ace' : 11}

TRUMP_POINTS = {'nine' : 17,
                 'jack' : 26,
                 'ten' : 10,
                 'ace' : 11}

NUM_PLAYERS = 4

NUM_ROUNDS = len(SUITS) * len(NORMAL_POINTS) // NUM_PLAYERS

CLOSED_CARDS = NUM_ROUNDS // 2
OPEN_CARDS = NUM_ROUNDS - CLOSED_CARDS