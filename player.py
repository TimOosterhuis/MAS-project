import random
from rules_config import playable



class Player:
    def __init__(self, team, c_cards, o_cards, turn, name):
        self.team = team
        self.closed_cards = c_cards
        self.open_cards = o_cards
        self.turn = turn
        self.name = name
        # en dan self knowledge = get_knowledge_from(open_cards, closed_cards)

    def play_card(self, trick = None):
        cards = playable(self.open_cards + self.closed_cards, self.team, trick)
        card = cards[random.randint(0, len(cards) - 1)]
        if card in self.open_cards:
            self.open_cards.remove(card)
        else:
            self.closed_cards.remove(card)
        return card