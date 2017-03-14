
class Player():
    def __init__(self, team, c_cards, o_cards, lead):
        self.team = team
        self.closed_cards = c_cards
        self.open_cards = o_cards
        self.lead = lead
        # en dan self knowledge = get_knowledge_from(open_cards, closed_cards)

    def play_card(self):
        pass