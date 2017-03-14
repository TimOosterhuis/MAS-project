import random
from rules_config import playable



class Player:
    def __init__(self, team, turn, name):
        self.team = team
        self.closed_cards = []
        self.open_cards = []
        self.turn = turn
        self.name = name
        self.knowledge = []
        # en dan self knowledge = get_knowledge_from(open_cards, closed_cards)

    def play_card(self, trick = None):
        cards = playable(self.open_cards + self.closed_cards, self.team, trick)
        print('playable cards for ' + self.name + ' are ' + str(cards))

        #print("\n---HERE A PLAYER NEEDS TO DEVISE ITS BEST STRATEGY---\n")

        card = cards[random.randint(0, len(cards) - 1)]
        if card in self.open_cards:
            self.open_cards.remove(card)
        else:
            self.closed_cards.remove(card)
        return card