import random
from rules_config import playable



class Player:
    def __init__(self, team, c_cards, o_cards, turn):
        self.team = team
        self.closed_cards = c_cards
        self.open_cards = o_cards
        self.turn = turn
        # en dan self knowledge = get_knowledge_from(open_cards, closed_cards)

    def play_card(self, trick = None):
        cards = playable(self.open_cards + self.closed_cards, self.team, trick)
        return cards[random.randint(len(cards))]