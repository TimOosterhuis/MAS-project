#  from rules_config import *
from rules_config_big import *
from player import *
from trick import Trick
import random

debug = False

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
    player_1 = Player(Team('South', 'North', '1'), 0, 'South', cards)
    player_2 = Player(Team('East', 'West', '2'), 1, 'East', cards)
    player_3 = Player(Team('South', 'North', '1'), 2, 'North', cards)
    player_4 = Player(Team('East', 'West', '2'), 3, 'West', cards)

    players = [player_1, player_2, player_3, player_4]

    common_knowledge = []
    idx = 0
    idx2 = CLOSED_CARDS
    #assert CLOSED_CARDS == OPEN_CARDS
    for player in players:  #  Card division between players
        player.closed_cards = cards[idx:idx2]
        idx = idx2
        idx2 += OPEN_CARDS
        player.open_cards = cards[idx:idx2]
        for open_card in player.open_cards:  #  Add open cards to common knowledge
            common_knowledge.append((player, open_card, False))
        idx = idx2
        idx2 += CLOSED_CARDS
        print(str(player.name) + ' has ' + str(player.closed_cards) + ' and ' + str(player.open_cards))
        #print(str(player.name) + ' has ' + str(len(player.closed_cards)) + ' closed cards and ' + str(len(player.open_cards)) + ' open cards')

    for player in players:  #  Knowledge init
        player.knowledge.extend(common_knowledge)
        for closed_card in player.closed_cards:
            player.knowledge.append((player, closed_card, False))
        #player.update_card_knowledge(trump)
        player.create_possibles()
        if debug:
            print(player.name, " knows (initial) ",player.knowledge)

    score = {'1' : 0, '2' : 0}
    #  First rounds                               HERE THE GAME BEGINS!!!!!!!!!!!!!!!!!!!
    for round in range(NUM_ROUNDS-1):
        print('\nnew round')  # First player plays a card here
        trick = Trick(trump, players[0], players[0].play_card(trump))
        print(str(players[0].name) + ' plays ' + str(trick.cards[-1]))

        for player in players:  #  Knowledge update
            try:
                player.knowledge.remove((players[0], trick.cards[-1], False))
            except ValueError:
                pass
            player.knowledge.append((players[0], trick.cards[-1],True))
            player.update_possibles(trick)
            if debug:
                print(player.name + ' Knows (update): ' + str(player.knowledge))

        for player in players[1:]: # Each following player picks card to play and plays
            trick.add_card(player, player.play_card(trump, trick))
            print(str(player.name) + ' plays ' + str(trick.cards[-1]))

            for pla in players:  #  Knowledge update
                try:
                    pla.knowledge.remove((player, trick.cards[-1], False))
                except ValueError:
                    pass
                pla.knowledge.append((player, trick.cards[-1], True))
                pla.update_possibles(trick)
                if debug:
                    print(pla.name + ' Knows (update): ' + str(pla.knowledge))
                #player.update_card_knowledge(trump, trick)

        trick.check_bonus()
        score[trick.winner.team] += int(trick.score)  #  Score is added to winning team
        print(str(trick.winner.name) + ' wins the trick with highest card ' + str(trick.high_card) + ', trick score ' + str(int(trick.score)))
        players = players[trick.winner.turn:] + players[:trick.winner.turn]  #  Winning player is new starter
        #print(players[0].name, players[1].name, players[2].name, players[3].name)
        for i in range(NUM_PLAYERS):
            players[i].turn = i

    #  Last round
    print('\nlast round')
    trick = Trick(trump, players[0], players[0].play_card(trump))
    print(str(players[0].name) + ' plays ' + str(trick.cards[-1]))

    for player in players:  #  knowledge update
        try:
            player.knowledge.remove((players[0], trick.cards[-1], False))
        except ValueError:
            pass
        player.knowledge.append((players[0], trick.cards[-1], True))
        player.update_possibles(trick)
        if debug:
            print(player.name + ' Knows (update): ' + str(player.knowledge))

    for player in players[1:]:  # Each following player picks card to play and plays
        trick.add_card(player, player.play_card(trump, trick))
        print(str(player.name) + ' plays ' + str(trick.cards[-1]))

        for pla in players:  #  Knowledge update
            try:
                pla.knowledge.remove((player, trick.cards[-1], False))
            except ValueError:
                pass
            pla.knowledge.append((player, trick.cards[-1], True))
            pla.update_possibles(trick)
            #player.update_card_knowledge(trump, trick)
            if debug:
                print(pla.name + ' Knows (update): ' + str(pla.knowledge))

    trick.check_bonus()
    score[trick.winner.team] += int(trick.score+10)  # Final round is worth 10 points
    print(str(trick.winner.name) + ' wins the trick with highest card ' + str(
        trick.high_card) + ', trick score ' + str(int(trick.score+10)))
    players = players[trick.winner.turn:] + players[:trick.winner.turn]
    # print(players[0].name, players[1].name, players[2].name, players[3].name)
    for i in range(NUM_PLAYERS):
        players[i].turn = i

    print(score)

    pit = False
    total = score['1']+score['2']
    if score['1'] == 0:
        score['2'] = total + 100
        print('team 2: PIT!')
        pit = True
    elif score['2'] == 0:
        score['1'] = total + 100
        print('team 1: PIT!')
        pit = True

    if score['1'] <= (total/2) and not pit:
        print('team 1: NAT!')
        score['1'] = 0
        score['2'] = total


    print(score)






if __name__ == "__main__":
    main()