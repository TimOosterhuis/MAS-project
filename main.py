#  from rules_config import *
from rules_config_big import *
from player import *
from trick import Trick
import random
import pygame
from image import *

#-----------------------------------------------------------------------------------------------------------------------
#Main, plays through one iteration of a game of klaverjassen
#-----------------------------------------------------------------------------------------------------------------------

def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen_size = (1200, 800)  # place_holder for board size
    game_display = pygame.display.set_mode((screen_size[0], screen_size[1]))
    game_display.fill((205,205,255))
    pygame.display.update()
    #while not game_over:
    pygame.time.wait(1000)

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

    common_knowledge = [('GAME_RULE_TRUMP', trump, True)]
    idx = 0
    idx2 = CLOSED_CARDS
    #assert CLOSED_CARDS == OPEN_CARDS
    for player in players:  #  Card division between players
        player.closed_cards = cards[idx:idx2]
        idx = idx2
        idx2 += OPEN_CARDS
        player.open_cards = cards[idx:idx2]
        for open_card in player.open_cards:  #  Add open cards to common knowledge
            common_knowledge.append((player.name, open_card, False))
        idx = idx2
        idx2 += CLOSED_CARDS
        print(str(player.name) + ' has ' + str(player.closed_cards) + ' and ' + str(player.open_cards))
        #print(str(player.name) + ' has ' + str(len(player.closed_cards)) + ' closed cards and ' + str(len(player.open_cards)) + ' open cards')

    for player in players:  #  Knowledge init
        player.knowledge.extend(common_knowledge)
        for closed_card in player.closed_cards:
            player.knowledge.append((player.name, closed_card, False))
        player.create_possibles()
        if debug:
            print(player.name + " knows (initial) " + str(player.knowledge))

    score = {'1' : 0, '2' : 0}
    #  First rounds                               HE RE THE GAME BEGINS!!!!!!!!!!!!!!!!!!!
    game_pause = True
    for round in range(NUM_ROUNDS-1):
        for player in players: # Each following player picks card to play and plays
            round = True
            while round:
                run_one_frame = False
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            game_pause = not game_pause
                            print('PAUSED ' + str(game_pause))
                        if event.key == pygame.K_RIGHT:
                            run_one_frame = True
                if not game_pause or run_one_frame:
                    game_display.fill((205, 205, 255))
                    for i in range(len(player.closed_cards)):
                        card = player.closed_cards[i]
                        file_name = IMAGE_DICT[card[1]] + IMAGE_DICT[card[0]] + '.gif'
                        image, im_rect = load_image(file_name)
                        print('TESTING ' + str(im_rect))
                        x_offset = screen_size[0]/2 - 20 * len(player.closed_cards) + 20*i
                        game_display.blit(image, (x_offset, screen_size[1] * (3/4)))
                        pygame.display.update()
                        print(x_offset, screen_size[1] * (3/4))
                    pygame.display.flip()
                    if player == players[0]:
                        print('\nnew round')  # First player plays a card here
                        trick = Trick(trump, players[0], players[0].play_card(trump))
                    else:
                        trick.add_card(player, player.play_card(trump, trick))
                    print(player.name + ' plays ' + str(trick.cards[-1]))

                    for pla in players:  #  Knowledge update for all players
                        try:
                            pla.knowledge.remove((player, trick.cards[-1], False))
                        except ValueError:
                            pass
                        pla.knowledge.append((player, trick.cards[-1], True))
                        pla.update_possibles(trick)
                        if debug:
                            print(pla.name + ' Knows (update): ' + str(pla.knowledge))
                    if not game_pause or run_one_frame:
                        round = False
        trick.check_bonus()
        score[trick.winner.team.nr] += int(trick.score)  #  Score is added to winning team
        print(trick.winner.name + ' wins the trick with highest card ' + str(trick.high_card) + ', trick score ' + str(int(trick.score)))
        players = players[trick.winner.turn:] + players[:trick.winner.turn]  #  Winning player is new starter
        for i in range(NUM_PLAYERS):
            players[i].turn = i


    #  Last round
    print('\nlast round')
    trick = Trick(trump, players[0], players[0].play_card(trump))
    print(players[0].name + ' plays ' + str(trick.cards[-1]))

    for player in players:  #  knowledge update
        try:
            player.knowledge.remove((players[0].name, trick.cards[-1], False))
        except ValueError:
            pass
        player.knowledge.append((players[0].name, trick.cards[-1], True))
        player.update_possibles(trick)
        if debug:
            print(player.name + ' Knows (update): ' + str(player.knowledge))

    for player in players[1:]:  # Each following player picks card to play and plays
        trick.add_card(player, player.play_card(trump, trick))
        print(player.name + ' plays ' + str(trick.cards[-1]))

        for pla in players:  #  Knowledge update
            try:
                pla.knowledge.remove((player.name, trick.cards[-1], False))
            except ValueError:
                pass
            pla.knowledge.append((player.name, trick.cards[-1], True))
            pla.update_possibles(trick)
            if debug:
                print(pla.name + ' Knows (update): ' + str(pla.knowledge))

    trick.check_bonus()
    score[trick.winner.team.nr] += int(trick.score+10)  # Final round is worth 10 points
    print(trick.winner.name + ' wins the trick with highest card ' + str(trick.high_card) + ', trick score ' + str(int(trick.score+10)))
    players = players[trick.winner.turn:] + players[:trick.winner.turn]
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






if __name__ == "__main__": # game loop
    main()
