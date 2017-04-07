import random
from rules_config import *
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
        notices = []
        if debug:
            print(self.name + ' holds for possible (before possible update): ' + str(self.possibles))
        # 1 Delete last trick card from possibles
        self.possibles = [chunk for chunk in self.possibles if trick.cards[-1] not in chunk]

        # 2 Inference if player does not have asked suit anymore (then delete this suit of that player from possibles)
        if trick.cards[-1][0] != trick.cards[0][0]:
            notices.append('Public announcement: ' + trick.players[-1].name + ' no longer has ' + trick.cards[0][0] + '!')
            self.possibles = [chunk for chunk in self.possibles if trick.players[-1].name not in chunk or trick.cards[0][0] not in chunk[1]]
            if trick.players[-1].team.nr != trick.winner.team.nr and trick.cards[-1][0] != trick.trump:  # Laatste speler gooit geen troef op en zit niet op winnende team
                if trick.high_card[0] == trick.trump:  # maar er is wel getroefd:
                    higher_trumps = [chunk for chunk in self.possibles if trick.players[-1].name in chunk and chunk[1][0] == trick.trump and chunk[1][2] > trick.high_card[2]]
                    self.possibles = [chunk for chunk in self.possibles if chunk not in higher_trumps ]
                    notices.append('Public announcement: ' + trick.players[-1].name + ' has no ' + trick.trump + ' higher than ' + trick.high_card[1] + '!')
                else: #  Nog niet getroefd, dus players[-1] heeft helemaal geen troef meer
                    self.possibles = [chunk for chunk in self.possibles if trick.players[-1].name not in chunk or chunk[1][0] != trick.trump]
                    notices.append('Public announcement: ' + trick.players[-1].name + ' no longer has ' + trick.trump + '!')

        # 3 Inference if player plays card that is the card below the highest card, then he doesn't have any other
        suit_cards_left1 = [chunk[1] for chunk in self.knowledge if chunk[1][0] == trick.cards[0][0] and chunk[2] == False]
        suit_cards_left2 = [chunk[1] for chunk in self.possibles if chunk[1][0] == trick.cards[0][0] and chunk[2] == False]
        suit_cards_left1.extend(suit_cards_left2)
        suit_left = sorted(list(set(suit_cards_left1)), key=lambda tup: tup[2], reverse=True)
        if suit_left != []:
            if trick.cards[-1][0] == trick.cards[0][0] and trick.cards[-1][2] < trick.high_card[2] and trick.cards[-1][2] > suit_left[0][2]: # Player played highest possible non winning card of suit, so does not have any other
                self.possibles = [chunk for chunk in self.possibles if trick.players[-1].name not in chunk or trick.cards[0][0] not in chunk[1]]
                notices.append('Public announcement: ' + trick.players[-1].name + ' no longer has ' + trick.cards[0][0] + ' lower than ' + trick.cards[-1][1] + '!')


        # 4 Inference if card is only possible for one player, delete card from possibles, add card to knowledge
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
        return notices