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

def draw_model(screen, players, card, left, top, width, height):
    for player in players:
        world_node = pygame.Rect(left + HAS_CARD_DICT[player.name][0] * width, top + HAS_CARD_DICT[player.name][1] * height, 50, 50)
        print(world_node.left, world_node.top)
        if card in player.own_cards:
            true_card_owner = player.name
            pygame.draw.rect(screen, (225, 225, 0), world_node, 5)
        else:
            pygame.draw.rect(screen, (0, 0, 0), world_node, 1)
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
                start_pos = (left + HAS_CARD_DICT[true_card_owner][0] * width, top + HAS_CARD_DICT[true_card_owner][1] * height)
                end_pos = (left + HAS_CARD_DICT[relation[0]][0] * width, top + HAS_CARD_DICT[relation[0]][1] * height)
                pygame.draw.line(screen, REL_COLOR_DICT[player.name], start_pos, end_pos, 2)




