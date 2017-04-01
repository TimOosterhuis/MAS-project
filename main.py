#  from rules_config import *
from rules_config_big import *
from player import *
from trick import Trick
import random
import pygame
from image import *
from model import draw_model

#-----------------------------------------------------------------------------------------------------------------------
#Main, plays through one iteration of a game of klaverjassen
#-----------------------------------------------------------------------------------------------------------------------

def main():
    pygame.init()
    pygame.font.init()
    name_font = pygame.font.SysFont('arial', 20)
    message_font = pygame.font.SysFont('arial', 16)
    clock = pygame.time.Clock()
    screen_size = (900, 600)  # place_holder for board size
    diagram_width = 600
    message_screen_height = 100
    game_display = pygame.display.set_mode((screen_size[0] + diagram_width, screen_size[1] + message_screen_height))
    game_display.fill((205, 205, 255), pygame.Rect(0, 0, screen_size[0], screen_size[1]))
    game_display.fill((255, 255, 255), pygame.Rect(screen_size[0] + 2, 0, diagram_width, screen_size[1]))
    game_display.fill((255, 255, 255), pygame.Rect(0, screen_size[1] + 2, screen_size[0] + diagram_width, message_screen_height))
    pygame.display.update()
    #while not game_over:
    pygame.time.wait(1000)

    #initialize randomized cards and trump
    trump = SUITS[random.randint(0,3)]
    print(str(trump) + ' is trump')
    ordered_cards = []
    cards = []
    for suit in SUITS:
        ranks = NORMAL_POINTS if suit != trump else TRUMP_POINTS
        for rank in ranks:
            ordered_cards.append((suit, rank, ranks[rank]))
    cards = list(ordered_cards)
    random.shuffle(cards)
    # print(cards)
    # initialize players
    assert NUM_PLAYERS == 4
    player_1 = Player(Team('South', 'North', '1'), 0, 'South', cards)
    player_2 = Player(Team('East', 'West', '2'), 1, 'West', cards)
    player_3 = Player(Team('South', 'North', '1'), 2, 'North', cards)
    player_4 = Player(Team('East', 'West', '2'), 3, 'East', cards)

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
        player.own_cards = list(player.closed_cards + player.open_cards)
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
    #  First rounds                               HE RE THE GAME BEGINS!!!!!!!!!!!!!!!!!!
    game_pause = True
    for game_round in range(NUM_ROUNDS):

        game_display.fill((205, 205, 255), pygame.Rect(0, 0, screen_size[0], screen_size[1]))

        for i in range(len(PLAYERS)):
            name_display = name_font.render(PLAYERS[i], 1, (0, 0, 0))
            game_display.blit(name_display, name_pos(PLAYERS[i], 8, screen_size))

        trump_display = name_font.render(str(trump) + ' is trump', 1, (0, 0, 0))
        open_close_info = 'Game with ' + str(OPEN_CARDS) + ' open cards and ' + str(CLOSED_CARDS) + ' cards.'
        open_close_display = message_font.render(open_close_info, 1, (0, 0, 0))
        continue_info1 = 'Press right arrow to continue'
        continue_info2 = 'Press space bar to skip to end and close'
        continue_display1 = message_font.render(continue_info1, 1, (0, 0, 0))
        continue_display2 = message_font.render(continue_info2, 1, (0, 0, 0))

        score_update1 = 'South and North:  ' + str(score['1'])
        score_update2 = 'East and West:    ' + str(score['2'])
        score_update_display1 = message_font.render(score_update1, 1, (0, 0, 0))
        score_update_display2 = message_font.render(score_update2, 1, (0, 0, 0))
        game_display.blit(score_update_display1, (20, screen_size[1]-50))
        game_display.blit(score_update_display2, (20, screen_size[1]-35))


        game_display.blit(trump_display, (10, 10))
        game_display.blit(open_close_display, (10, 35))
        game_display.blit(continue_display1, (600, 10))
        game_display.blit(continue_display2, (600, 25))

        game_display.fill((255, 255, 255), pygame.Rect(screen_size[0] + 2, 0, diagram_width, screen_size[1]))

        model_title = 'Card knowledge of the current player:'
        model_title_display = name_font.render(model_title, 1, (0, 0, 0))
        game_display.blit(model_title_display, (screen_size[0] + 10, 10))
        dropdown = pygame.Rect(screen_size[0] + 10, 35, 150, 20)
        pygame.draw.rect(game_display, (0, 0, 0), dropdown, 1)
        dropdown_display = message_font.render('choose a card', 1, (0, 0, 0))
        game_display.blit(dropdown_display, ((dropdown.left + 5), dropdown.top))

        for player in players: # Each following player picks card to play and plays
            turn = True
            menu_open = False
            select_available = False
            while turn:

                if player == players[0] and game_round == 0:
                    run_one_frame = True
                else:
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
                x, y = pygame.mouse.get_pos()
                #print(x, y)
                m_pressed = pygame.mouse.get_pressed()
                x_hover_dropdown = dropdown.left < x < dropdown.left + dropdown.width
                y_hover_dropdown = dropdown.top < y < dropdown.top + dropdown.height
                if x_hover_dropdown and y_hover_dropdown and m_pressed[0]:
                    for i in range(1, len(ordered_cards) + 1):
                        dropdown_opt = pygame.Rect(screen_size[0] + 10, 35 + 20*i, 150, 20)
                        pygame.draw.rect(game_display, (255, 255, 255), dropdown_opt, 0)
                        pygame.draw.rect(game_display, (0, 0, 0), dropdown_opt, 1)
                        card = ordered_cards[i - 1]
                        card_display = message_font.render(card[1] + ' of ' + card[0], 1, (0, 0, 0))
                        game_display.blit(card_display, ((dropdown_opt.left + 5), dropdown_opt.top))
                    pygame.display.update()
                    menu_open = True
                if menu_open and not m_pressed[0]:
                    select_available = True
                if select_available and m_pressed[0]:
                    game_display.fill((255, 255, 255), pygame.Rect(screen_size[0] + 2, 55, diagram_width, screen_size[1] + message_screen_height - 55))
                    pygame.draw.line(game_display, (0, 0, 0), (screen_size[0], screen_size[1]), (screen_size[0] + diagram_width, screen_size[1]), 2)
                    if x_hover_dropdown and dropdown.top + dropdown.height < y:
                        i = int((y - 35) / 20 - 1)
                        card = ordered_cards[i]
                        picked_card = message_font.render('card is: ' + card[1] + ' of ' + card[0], 1, (0, 0, 0))
                        game_display.blit(picked_card, (screen_size[0] + 50, 100))
                        draw_model(game_display, players, message_font, card, screen_size[0], 55, diagram_width, screen_size[1] - 55)
                    pygame.display.update()
                    select_available = False
                if not game_pause or run_one_frame:
                    clear_hands(game_display, (205, 205, 255), len(player.closed_cards)+len(player.open_cards), screen_size)
                    game_display.fill((255, 255, 255), pygame.Rect(screen_size[0] + 2, 55, diagram_width, screen_size[1] - 55))

                    for pla in players:

                        for i in range(len(pla.closed_cards)):   # Draw hands closed cards
                            card = pla.closed_cards[i]
                            if pla == player:
                                file_name = IMAGE_DICT[card[1]] + IMAGE_DICT[card[0]] + '.gif'
                            else:
                                file_name = 'b.gif'
                            image, im_rect = load_image(file_name)
                            game_display.blit(image, calc_offset(pla.name, len(pla.closed_cards)+len(pla.open_cards), screen_size, i))

                        for i in range(len(pla.open_cards)):
                            card = pla.open_cards[i]
                            if pla == player:
                                file_name = IMAGE_DICT[card[1]] + IMAGE_DICT[card[0]] + '.gif'
                            else:
                                file_name = IMAGE_DICT[card[1]] + IMAGE_DICT[card[0]] + '.gif'
                            image, im_rect = load_image(file_name)
                            game_display.blit(image, calc_offset(pla.name, len(pla.closed_cards)+len(pla.open_cards), screen_size, i+len(pla.closed_cards)))

                        pygame.display.update()
                    if game_pause:
                        pygame.time.delay(1000)
                    clear_hands(game_display, (205, 205, 255), len(player.closed_cards) + len(player.open_cards),
                                screen_size)


                    if player == players[0]:
                        print('\nnew round')  # First player plays a card here
                        card, thoughts = players[0].play_card(trump)
                        trick = Trick(trump, players[0], card)
                    else:
                        card, thoughts = player.play_card(trump, trick)
                        trick.add_card(player, card)
                    #
                    game_display.fill((255, 255, 255), pygame.Rect(0, screen_size[1] + 2, screen_size[0] + diagram_width, message_screen_height))
                    for i in range(len(thoughts)):
                        message = message_font.render(thoughts[i], 1, (0, 0, 0))
                        game_display.blit(message, (10, screen_size[1] + 10 + (i * 20)))
                    # Draw trick
                    card = trick.cards[-1]
                    file_name = IMAGE_DICT[card[1]] + IMAGE_DICT[card[0]] + '.gif'
                    image, im_rect = load_image(file_name)
                    game_display.blit(image, (screen_size[0]/2 + CENTER_POS[player.name][0], screen_size[1]/2 + CENTER_POS[player.name][1]))

                    print(player.name + ' plays ' + str(trick.cards[-1]))


                    for pla in players:

                        for i in range(len(pla.closed_cards)):   # Draw hands closed cards
                            card = pla.closed_cards[i]
                            if pla == player:
                                file_name = IMAGE_DICT[card[1]] + IMAGE_DICT[card[0]] + '.gif'
                            else:
                                file_name = 'b.gif'
                            image, im_rect = load_image(file_name)
                            game_display.blit(image, calc_offset(pla.name, len(pla.closed_cards)+len(pla.open_cards), screen_size, i))

                        for i in range(len(pla.open_cards)):
                            card = pla.open_cards[i]
                            if pla == player:
                                file_name = IMAGE_DICT[card[1]] + IMAGE_DICT[card[0]] + '.gif'
                            else:
                                file_name = IMAGE_DICT[card[1]] + IMAGE_DICT[card[0]] + '.gif'
                            image, im_rect = load_image(file_name)
                            game_display.blit(image, calc_offset(pla.name, len(pla.closed_cards)+len(pla.open_cards), screen_size, i+len(pla.closed_cards)))

                        pygame.display.update()

                        try:  #  Knowledge update for all players
                            pla.knowledge.remove((trick.players[-1].name, trick.cards[-1], False))
                        except ValueError:
                            pass
                        pla.knowledge.append((trick.players[-1].name, trick.cards[-1], True))
                        pla.update_possibles(trick)

                        if debug:
                            print(pla.name + ' Knows (update): ' + str(pla.knowledge))

                    if game_pause:
                        pygame.time.delay(1500)

                    if player.turn == 3:
                        trick.check_bonus()

                        if game_round == (NUM_ROUNDS - 1):
                            score[trick.winner.team.nr] += int(trick.score + 10)  # Final round is worth 10 points
                            end = trick.winner.name + ' wins the final trick with highest card ' + str(
                                trick.high_card) + ', trick score ' + str(int(trick.score + 10))
                            print(end)
                            end_display = message_font.render(end, 1, (0, 0, 0))
                            game_display.blit(end_display, (10, screen_size[1] + message_screen_height - 25))

                        else:
                            score[trick.winner.team.nr] += int(trick.score)  # Score is added to winning team
                            end = trick.winner.name + ' wins the trick with highest card ' + str(
                                trick.high_card) + ', trick score ' + str(int(trick.score))
                            print(end)
                            end_display = message_font.render(end, 1, (0, 0, 0))
                            game_display.blit(end_display, (10, screen_size[1] + message_screen_height - 25))

                        pygame.display.update()


                    if not game_pause or run_one_frame:
                        turn = False




        players = players[trick.winner.turn:] + players[:trick.winner.turn]  #  Winning player is new starter
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

    game_display.fill((205, 205, 255), pygame.Rect(20, screen_size[1] - 50, 150, 30))
    pygame.display.update()
    score_update1 = 'South and North:  ' + str(score['1'])
    score_update2 = 'East and West:    ' + str(score['2'])
    score_update_display1 = message_font.render(score_update1, 1, (0, 0, 0))
    score_update_display2 = message_font.render(score_update2, 1, (0, 0, 0))
    game_display.blit(score_update_display1, (20, screen_size[1] - 50))
    game_display.blit(score_update_display2, (20, screen_size[1] - 35))
    pygame.display.update()
    pygame.time.delay(2500)






if __name__ == "__main__": # game loop
    main()
