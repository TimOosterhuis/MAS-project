from rules_config import *
from player import Player
from trick import Trick
import random

def main():
    #initialize randomized cards and trump
    trump = SUITS[random.randint(0,3)]
    print(str(trump) + ' is trump')
    cards = []
    for suit in SUITS:
        ranks = NORMAL_POINTS if suit != trump else TRUMP_POINTS
        for rank in ranks:
            cards.append((suit, rank, ranks[rank]))
    random.shuffle(cards)
    # print(cards)
    # initialize players
    assert NUM_PLAYERS == 4
    player_1 = Player('s', [], [], 0, 'player south')
    player_2 = Player('e', [], [], 1, 'player east')
    player_3 = Player('n', [], [], 2, 'player north')
    player_4 = Player('w', [], [], 3, 'player west')
    players = [player_1, player_2, player_3, player_4]
    idx = 0
    idx2 = CLOSED_CARDS
    assert CLOSED_CARDS == OPEN_CARDS
    for player in players:
        player.closed_cards = cards[idx:idx2]
        idx = idx2
        idx2 += CLOSED_CARDS
        player.open_cards = cards[idx:idx2]
        idx = idx2
        idx2 += CLOSED_CARDS
        print(str(player.name) + ' has ' + str(player.closed_cards) + ' and ' + str(player.open_cards))
    #     print(player.open_cards)
    # print(player_4.open_cards)

    score = {'1' : 0, '2' : 0}
    for round in range(NUM_ROUNDS):
        trick = Trick(trump, players[0], players[0].play_card())
        print('new round')
        print(str(players[0].name) + ' plays ' + str(trick.cards[-1]))
        for player in players[1:]:
            trick.add_card(player, player.play_card(trick))
            print(str(player.name) + ' plays ' + str(trick.cards[-1]))
        score[trick.winner.team] += trick.score
        print(str(trick.winner.name) + ' wins the trick, trick score ' + str(trick.score))
        players = players[trick.winner.turn:] + players[:trick.winner.turn]
        print(players[0].name, players[1].name, players[2].name, players[3].name)
        for i in range(NUM_PLAYERS):
            players[i].turn = i
    print(score)





if __name__ == "__main__":
    main()