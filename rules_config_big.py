SUITS = ['Hearts', 'Spades', 'Diamonds', 'Clubs']

NORMAL_POINTS = {'seven' : 0.001,
                 'eight' : 0.002,
                 'nine' : 0.003,
                 'jack' : 2.000,
                 'queen' : 3.000,
                 'king' : 4.000,
                 'ten' : 10.000,
                 'ace' : 11.000}

TRUMP_POINTS = {'seven' : 0.001,
                'eight' : 0.002,
                'queen' : 3.000,
                'king' : 4.000,
                'ten' : 10.000,
                'ace' : 11.000,
                'nine' : 14.000,
                'jack' : 20.000}

NUM_PLAYERS = 4

NUM_ROUNDS = len(SUITS) * len(NORMAL_POINTS) // NUM_PLAYERS

CLOSED_CARDS = NUM_ROUNDS // 2 # Changeable by will
OPEN_CARDS = NUM_ROUNDS - CLOSED_CARDS


def playable(cards, team, trick = None):
    if trick:
        #print('high card is ' + str(trick.high_card) + ', team is ' + trick.winner.team)
        trump_cards = [card for card in cards if card[0] == trick.trump]
        #print("Trump cards are" +  str(trump_cards))
        # print(trick.cards[0][0] + " gevraagd")
        if trick.high_card[0] == trick.trump: # Er is begonnen met troef of ingetroefd
            higher_trump_cards = [card for card in trump_cards if card[2] > trick.high_card]
        else:
            higher_trump_cards = []

        if trick.cards[0][0] != trick.trump:  # Geen troef gevraagd
            suit_cards = [card for card in cards if card[0] == trick.cards[0][0]]
            if suit_cards != []:  # Player heeft nog suit
                playable_cards = suit_cards
            else:  # Player heeft geen suit meer
                if trick.winner.team != team and trump_cards != []:  # Player heeft troef en niet op winnende team
                    if higher_trump_cards != []:  # Speler kan overtroeven
                        playable_cards = higher_trump_cards
                    else:  # Speler kan introeven
                        playable_cards = trump_cards
                else:  # Player kan niet in- of overtroeven
                    playable_cards = cards
        else:  # Begonnen met troef gevraagd
            if higher_trump_cards != []:  # Player heeft hogere troef dan gespeelde troef
                playable_cards = higher_trump_cards
            elif trump_cards != []:  # Player heeft nog troef
                playable_cards = trump_cards
            else:  # Player heeft geen troef meer
                playable_cards = cards
    else:
        playable_cards = cards
    #print('playable cards are ' + str(playable_cards))
    return playable_cards

def old_playable(cards, team, trick = None):
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
