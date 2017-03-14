from rules_config import *
from player import Player
from trick import Trick
import random

def main():
    #initialize randomized cards and trump
    trump = SUITS[random.randint(0,3)]
    cards = []
    for suit in SUITS:
        ranks = NORMAL_POINTS if suit != trump else TRUMP_POINTS
        for rank in ranks:
            cards.append((suit, rank, ranks[rank]))
    random.shuffle(cards)
    # print(cards)
    # initialize players
    assert NUM_PLAYERS == 4
    player_1 = Player('1', [], [], 0)
    player_2 = Player('2', [], [], 1)
    player_3 = Player('1', [], [], 2)
    player_4 = Player('2', [], [], 3)
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
    #     print(player.closed_cards)
    #     print(player.open_cards)
    # print(player_4.open_cards)

    score = {'1' : 0, '2' : 0}
    for round in range(NUM_ROUNDS):
        trick = Trick(trump, players[0], players[0].play_card())
        for player in players[1:]:
            trick.add_card(player, player.play_card())
        score[trick.winner.team] += trick.score
        players = players[trick.winner.turn:] + player[:trick.winner.turn]
        for i in range(players):
            player.turn = i

    print(score)





if __name__ == "__main__":
    main()