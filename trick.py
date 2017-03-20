
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

    def check_bonus(self):
        if (self.trump, 'queen', 3) in self.cards and (self.trump, 'king', 4) in self.cards:
            self.score += 20
            print('Stuck, 20 points extra!')
        if(self.cards[0][0]==self.cards[1][0]==self.cards[2][0]==self.cards[3][0]):
            self.check_roem(self.cards)
        elif(self.cards[0][0]==self.cards[1][0]==self.cards[2][0]):
            self.check_roem([self.cards[0], self.cards[1], self.cards[2]])
        elif(self.cards[0][0]==self.cards[1][0]==self.cards[3][0]):
            self.check_roem([self.cards[0], self.cards[1], self.cards[3]])
        elif(self.cards[0][0]==self.cards[2][0]==self.cards[3][0]):
            self.check_roem([self.cards[0], self.cards[2], self.cards[3]])
        elif(self.cards[1][0]==self.cards[2][0]==self.cards[3][0]):
            self.check_roem([self.cards[1], self.cards[2], self.cards[3]])

    def check_roem(self, cards):
        dct = {'seven':1,
               'eight':2,
               'nine':3,
               'ten':4,
               'jack':5,
               'queen':6,
               'king':7,
               'ace':8}
        cards = [card[1] for card in cards]
        if len(cards)==4:
            sorts = sorted([dct[cards[0]], dct[cards[1]], dct[cards[2]], dct[cards[3]]])
            if sorts[0]+3 == sorts[-1]:
                self.score += 50
                print('Roem, 50 points extra!')
        else:
            sorts = sorted([dct[cards[0]], dct[cards[1]], dct[cards[2]]])
            if sorts[0]+2 == sorts[-1]:
                self.score += 20
                print('Roem, 20 points extra!')

