import random
from rules_config import *
#from rules_config_big import *

debug = True
PLAYERS = ['South','East','North','West']

class Player:
    def __init__(self, team, turn, name, cards):
        self.team = team
        self.closed_cards = []
        self.open_cards = []
        self.turn = turn
        self.name = name
        self.all_cards = cards
        self.knowledge = []
        self.possibles = []  #  could also be named self.unknowledge


    def play_card(self, trump, trick = None):
        cards = playable(self.open_cards + self.closed_cards, self.team, trick)
    #    print('playable cards for ' + self.name + ' are ' + str(cards))

    #    print("\n---HERE A PLAYER NEEDS TO DEVISE ITS BEST STRATEGY---\n")

        card = cards[random.randint(0, len(cards) - 1)]
        # best_Card = find_best_card(cards, self.team, self.knowledge, trick)
        if card in self.open_cards:
            self.open_cards.remove(card)
        else:
            self.closed_cards.remove(card)
        return card

    def create_possibles(self):
        unknown_cards = [card for card in self.all_cards if card not in [chunk[1] for chunk in self.knowledge]]
        for card in unknown_cards:
            for player in PLAYERS:
                if player != self.name:
                    self.possibles.append((player, card, False))
        if debug:
            print('\n' + self.name + ' holds for possible (initial): ' + str(self.possibles))

    def update_possibles(self, trick):
        if debug:
            print(self.name + ' holds for possible (before possible update): ' + str(self.possibles))
        # 1 Delete last trick card from possibles
        self.possibles = [chunk for chunk in self.possibles if trick.cards[-1] not in chunk]

        # 2 Inference if player does not have asked suit anymore (then delete this suit of that player from possibles)
        if trick.cards[-1][0] != trick.cards[0][0]:
            self.possibles = [chunk for chunk in self.possibles if trick.players[-1].name not in chunk and trick.cards[0][0] not in chunk[1]]

        # 3 Inference if card is only possible for one player, delete card from possibles, add card to knowledge
        single_cards = []
        possible_cards = [card[1] for card in self.possibles]
        for card in possible_cards:
            if possible_cards.count(card)==1:
                single_cards.append(card)

        for card in single_cards:
            for chunk in self.possibles:
                if card == chunk[1]:
                    self.knowledge.append(chunk)
        self.possibles = [chunk for chunk in self.possibles if chunk[1] not in single_cards]

        if debug:
            print(self.name + ' holds for possible (after possible update): ' + str(self.possibles))

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
            pass

        else:  #  There are no cards played, no inferences can be made
            pass



