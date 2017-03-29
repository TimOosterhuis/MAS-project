import random
#from rules_config import *
from rules_config_big import *
from tactics import *

#-----------------------------------------------------------------------------------------------------------------------
#Player and team class
#A player's knowledge about the game and what a player holds for possible in that game is modelled with two lists
#which the player updates with each trick played in main (a trick as a public announcement) uses to determine which card
#to play, for which it calls on tactics
#-----------------------------------------------------------------------------------------------------------------------


class Team:
    def __init__(self, first_player, second_player, nr):
        self.players = [first_player, second_player]
        self.nr = nr

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

class Player:
    def __init__(self, team, turn, name, cards):
        self.team = team
        self.closed_cards = []
        self.open_cards = []
        self.own_cards = []
        self.turn = turn
        self.name = name
        self.all_cards = cards
        self.knowledge = []  # gelijk aan K
        self.possibles = []  # gelijk aan M


    def play_card(self, trump, trick = None):
        cards = playable(self.open_cards + self.closed_cards, self.team, trick)
        print('playable cards for ' + self.name + ' are ' + str(cards))

        #card = cards[random.randint(0, len(cards) - 1)]
        card, thoughts = find_best_card(cards, self, trick)
        if card in self.open_cards:
            self.open_cards.remove(card)
        else:
            self.closed_cards.remove(card)
        return card, thoughts

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
            ## Changes from here.
            if trick.players[-1].team != trick.winner.team and trick.cards[-1][0] != trick.trump:  # Laatste speler gooit geen troef op en zit niet op winnende team
                if trick.high_card[0] == trick.trump:  # maar er is wel getroefd:
                    higher_trumps = [chunk for chunk in self.possibles if trick.players[-1].name in chunk and chunk[1][0] == trick.trump and chunk[1][2] > trick.high_card[2]]
                    self.possibles = [chunk for chunk in self.possibles if chunk not in higher_trumps ]
                else: #  Nog niet getroefd, dus players[-1] heeft helemaal geen troef meer
                    self.possibles = [chunk for chunk in self.possibles if trick.players[-1].name not in chunk and chunk[1][0] != trick.trump]

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