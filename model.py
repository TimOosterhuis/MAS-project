import pygame
from rules_config_big import *
from math import pi

HAS_CARD_DICT = {
    'South' : (1.0/3.0, 2.0/3.0),
    'West'  : (1.0/3.0, 1.0/3.0),
    'North' : (2.0/3.0, 1.0/3.0),
    'East'  : (2.0/3.0, 2.0/3.0),
}

REL_COLOR_DICT = {
    'South' : (255, 0, 0),
    'West'  : (0, 255, 0),
    'North' : (0, 0, 255),
    'East'  : (255, 0, 255),
}

REL_ARC_TO_SELF = {
    # first number represents the size of the arc, the two numbers after that represent the side of the world the arc starts at
    # 50 or zero depending on left/right, top/bottom, last two number represent the start and end radial angle to draw
    'South' : (10, 0, 50, 0.5*pi, 2*pi),
    'West'  : (20, 0, 0, 0.0, 1.5*pi),
    'North' : (30, 50, 0, -0.5*pi, pi),
    'East'  : (40, 50, 50, -pi, 0.5*pi),
}

REL_LINE_START = {
    'South' : (10, 50, 0, {'East' : (0, 1), 'West' : (-1, 0), 'North' : (-1, 0)}),
    'West'  : (20, 50, 50, {'South' : (-1, 0), 'East' : (0, -1), 'North' : (0, -1)}),
    'North' : (30, 0, 50, {'South' : (0, -1), 'West' : (0, -1), 'East' : (1, 0)}),
    'East'  : (40, 0, 0, {'South' : (0, 1), 'West' : (1, 0), 'North' : (1, 0)}),
}



def draw_model(screen, players, font, card, left, top, width, height):

    for player in players:
        legend = font.render(player.name, 1, REL_COLOR_DICT[player.name])
        screen.blit(legend, (left + 50, top + 45 + REL_ARC_TO_SELF[player.name][0] * 1.5))
        w_left = left + HAS_CARD_DICT[player.name][0] * width
        w_top = top + HAS_CARD_DICT[player.name][1] * height
        world_node = pygame.Rect(w_left, w_top, 50, 50)
        print(world_node.left, world_node.top)
        if card in player.own_cards:
            true_card_owner = player.name
            pygame.draw.rect(screen, (225, 225, 0), world_node, 5)
        else:
            pygame.draw.rect(screen, (0, 0, 0), world_node, 1)
        display_a = font.render(player.name, 1, (1, 1, 1))
        screen.blit(display_a, (w_left + 8, w_top))
        display_b = font.render('has', 1, (1, 1, 1))
        screen.blit(display_b, (w_left + 15, w_top + 15))
        display_c = font.render('card', 1, (1, 1, 1))
        screen.blit(display_c, (w_left + 12, w_top + 30))

    for player in players:
        relations = [world for world in player.knowledge if world[1] == card]
        relations.extend([world for world in player.possibles if world[1] == card])
        print(relations)
        for relation in relations:

            if true_card_owner == relation[0]:
                w_left = left + HAS_CARD_DICT[true_card_owner][0] * width - REL_ARC_TO_SELF[player.name][0] + REL_ARC_TO_SELF[true_card_owner][1]
                w_top = top + HAS_CARD_DICT[true_card_owner][1] * height - REL_ARC_TO_SELF[player.name][0] + REL_ARC_TO_SELF[true_card_owner][2]

                world_node = pygame.Rect(w_left, w_top, 2*REL_ARC_TO_SELF[player.name][0], 2*REL_ARC_TO_SELF[player.name][0])
                pygame.draw.arc(screen, REL_COLOR_DICT[player.name], world_node, REL_ARC_TO_SELF[true_card_owner][3],
                                REL_ARC_TO_SELF[true_card_owner][4], 2)
            else:
                w_start_l = left + HAS_CARD_DICT[true_card_owner][0] * width + (REL_LINE_START[player.name][0] * REL_LINE_START[true_card_owner][3][relation[0]][0]) + REL_LINE_START[true_card_owner][1]
                w_start_t = top + HAS_CARD_DICT[true_card_owner][1] * height + (REL_LINE_START[player.name][0] * REL_LINE_START[true_card_owner][3][relation[0]][1]) + REL_LINE_START[true_card_owner][2]
                w_stop_l = left + HAS_CARD_DICT[relation[0]][0] * width + (REL_LINE_START[player.name][0] * REL_LINE_START[relation[0]][3][true_card_owner][0]) + REL_LINE_START[relation[0]][1]
                w_stop_t = top + HAS_CARD_DICT[relation[0]][1] * height + (REL_LINE_START[player.name][0]  * REL_LINE_START[relation[0]][3][true_card_owner][1]) + REL_LINE_START[relation[0]][2]
                start_pos = (w_start_l, w_start_t)
                end_pos = (w_stop_l, w_stop_t)
                pygame.draw.line(screen, REL_COLOR_DICT[player.name], start_pos, end_pos, 2)




