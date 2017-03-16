import random
#  from rules_config import *
from rules_config_big import *

class Player:
    def __init__(self, team, turn, name):
        self.team = team
        self.closed_cards = []
        self.open_cards = []
        self.turn = turn
        self.name = name
        self.knowledge = []
        self.card_knowledge = []
        # en dan self knowledge = get_knowledge_from(open_cards, closed_cards)

    def play_card(self, trump, trick = None):
        cards = playable(self.open_cards + self.closed_cards, self.team, trick)
    #    print('playable cards for ' + self.name + ' are ' + str(cards))

    #    print("\n---HERE A PLAYER NEEDS TO DEVISE ITS BEST STRATEGY---\n")
        self.update_card_knowledge(trump)



        card = cards[random.randint(0, len(cards) - 1)]
        if card in self.open_cards:
            self.open_cards.remove(card)
        else:
            self.closed_cards.remove(card)
        return card

    def update_card_knowledge(self, trump):
        our_trumps = [card for card in self.knowledge if card[1][0] == trump and card[0].team == self.team]
        their_trumps  = [card for card in self.knowledge if card[1][0] == trump and card[0].team != self.team]

        known_trumps = [chunk for chunk in self.knowledge if chunk[1][0] == trump]
        played_trumps = [card for card in known_trumps if card[1][0] == trump and card[2] == True]
        unplayed_trumps = [card for card in known_trumps if card[1][0] == trump and card[2] == False]

        played_aces = [chunk for chunk in self.knowledge if chunk[1][0] != trump and chunk[2] == True and chunk[1][1] == 'ace']
        unplayed_aces = [chunk for chunk in self.knowledge if chunk[1][0] != trump and chunk[2] == False and chunk[1][1] == 'ace']



