import random
#  from rules_config import *
from rules_config_big import *

class Player:
    def __init__(self, team, turn, name, cards):
        self.team = team
        self.closed_cards = []
        self.open_cards = []
        self.turn = turn
        self.name = name
        self.all_cards = cards
        self.knowledge = []

        # en dan self knowledge = get_knowledge_from(open_cards, closed_cards)

    def play_card(self, trump, trick = None):
        cards = playable(self.open_cards + self.closed_cards, self.team, trick)
    #    print('playable cards for ' + self.name + ' are ' + str(cards))

    #    print("\n---HERE A PLAYER NEEDS TO DEVISE ITS BEST STRATEGY---\n")

        card = cards[random.randint(0, len(cards) - 1)]
        if card in self.open_cards:
            self.open_cards.remove(card)
        else:
            self.closed_cards.remove(card)
        return card

    def update_card_knowledge(self, trump, trick = None):
        ##  General knowledge about cards
        our_trumps = [card for card in self.knowledge if card[1][0] == trump and card[0].team == self.team]
        their_trumps = [card for card in self.knowledge if card[1][0] == trump and card[0].team != self.team]

        all_trumps = [card for card in self.all_cards if card[0] == trump]
        known_trumps = [chunk for chunk in self.knowledge if chunk[1][0] == trump]
        played_trumps = [card for card in known_trumps if card[2] == True]
        unplayed_trumps = [card for card in known_trumps if card[2] == False]

        unknown_trump_cards = [card for card in all_trumps if card not in [chunk[1] for chunk in known_trumps]]

        if trick:  #  cards are played, inferences can be made


        else:  #  There are no cards played, no inferences can be made
            pass



