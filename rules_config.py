
#-----------------------------------------------------------------------------------------------------------------------
#Rules_config, contains hardcoded definitions of the possible cards, points and other parameters, such as nr of players
#and closed cards
#also contains function to determine legally playable cards
#-----------------------------------------------------------------------------------------------------------------------
debug = False
explain = False
fast = True
fixed_hands = False # fixing the hands for bugtesting or demonstration of the different features

SUITS = ['Hearts', 'Spades', 'Diamonds', 'Clubs']

PLAYERS = ['South','East','North','West']

FACES = ['ace', 'king', 'queen', 'jack', 'ten', 'nine', 'eight', 'seven']

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

CLOSED_CARDS = 8 # Changeable by will
OPEN_CARDS = NUM_ROUNDS - CLOSED_CARDS


def playable(cards, team, trick = None):
    if trick:
    #    print('high card is ' + str(trick.high_card) + ', team is ' + trick.winner.team)
        trump_cards = [card for card in cards if card[0] == trick.trump]
    #    print("Trump cards are" +  str(trump_cards))
    #    print(trick.cards[0][0] + " gevraagd")
        if trick.high_card[0] == trick.trump: # Er is begonnen met troef of ingetroefd
            higher_trump_cards = [card for card in trump_cards if card[2] > trick.high_card[2]]
    #        print higher_trump_cards
        else:
            higher_trump_cards = []

        if trick.cards[0][0] != trick.trump:  # Geen troef gevraagd
            suit_cards = [card for card in cards if card[0] == trick.cards[0][0]]
            if suit_cards != []:  # Player heeft nog suit
                playable_cards = suit_cards
            else:  # Player heeft geen suit meer
                if trick.winner.team.nr != team.nr:  # partner heeft niet hoogste kaart (of nog geen partner gespeeld)

                    if trick.high_card[0] == trick.trump:  # als er is ingetroefd
                        if higher_trump_cards != []:  # player kan overtroeven
                            playable_cards = higher_trump_cards
                        else:  # player kan niet overtroeven
                            playable_cards = cards
                    else:  # niet ingetroefd of begonnen met troef
                        if trump_cards != []:  # Player heeft nog troef
                            playable_cards = trump_cards
                        else:
                            playable_cards = cards
                else:  # partner heeft hoogste kaart
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
