
class Trick:
    def __init__(self, trump, player, card):
        self.cards = [card]
        self.score = card[2]
        self.winner = player
        self.high_card = card
        self.trump = trump
        self.players = [player]
        #self.trumped = 0 if card[0] != trump else 1

    def add_card(self, player, card):
        self.cards.append(card)
        self.players.append(player)
        self.score += card[2]
        if (card[2] > self.high_card[2] and card[0] == self.high_card[0]) or (card[0] == self.trump and self.high_card[0] != self.trump):
            self.winner = player
            self.high_card = card
