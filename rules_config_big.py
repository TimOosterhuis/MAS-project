SUITS = ['Hearts', 'Spades', 'Diamonds', 'Clubs']

NORMAL_POINTS = {'seven' : 0,
                 'eight' : 0,
                 'nine' : 0,
                 'jack' : 2,
                 'queen' : 3,
                 'king' : 4,
                 'ten' : 10,
                 'ace' : 11}

TRUMP_POINTS = {'seven' : 0,
                'eight' : 0,
                'queen' : 3,
                'king' : 4,
                'ten' : 10,
                'ace' : 11,
                'nine' : 14,
                'jack' : 20}

NUM_PLAYERS = 4

NUM_ROUNDS = len(SUITS) * len(NORMAL_POINTS) // NUM_PLAYERS

CLOSED_CARDS = NUM_ROUNDS // 2 # Changeable by will
OPEN_CARDS = NUM_ROUNDS - CLOSED_CARDS


def playable(cards, team, trick = None):
    if trick:
        print('high card is ' + str(trick.high_card) + ', team is ' + trick.winner.team)
        trump_cards = [card for card in cards if card[0] == trick.trump]
        if trick.high_card[2] != trick.trump:
            suit_cards = [card for card in cards if card[0] == trick.high_card[0]]
            if suit_cards != []:
                playable_cards = suit_cards
            else:
                if trick.winner.team != team and trump_cards != []:
                    playable_cards = trump_cards
                else:
                    playable_cards = cards
        else:
            high_trump_cards = [card for card in trump_cards if card[2] > trick.high_card]
            if trick.winner.team != team and high_trump_cards != []:
                playable_cards = high_trump_cards
            else:
                playable_cards = cards
    else:
        playable_cards = cards
    #print('playable cards are ' + str(playable_cards))
    return playable_cards