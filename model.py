import pygame
from rules_config_big import *

HAS_CARD_DICT = {
    'South' : (1/3, 2/3),
    'West'  : (1/3, 1/3),
    'North' : (2/3, 1/3),
    'East'  : (2/3, 2/3),
}

REL_COLOR_DICT = {
    'South' : (255, 0, 0),
    'West'  : (0, 255, 0),
    'North' : (0, 0, 255),
    'East'  : (255, 0, 255),
}

REL_ARC_TO_SELF = {
    # first number represents the size of the arc, the two numbers after that represent the side of the world the arc starts at
    # -25 or zero depending on left/right, top/bottom, last two number represent the start and end radial angle to draw
    'South' : (10, -25, 0, 0, 270),
    'West'  : (20, -25, -25, 90, 0),
    'North' : (30, 0, -25, 180, 90),
    'East'  : (40, 0, 0, 270, 180),
}

def draw_model(screen, players, card, left, top, width, height):
    for player in players:
        world_node = pygame.Rect(left + HAS_CARD_DICT[player.name][0] * width, top + HAS_CARD_DICT[player.name][1] * height, 50, 50)
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
                world_node = pygame.Rect(left + HAS_CARD_DICT[true_card_owner][0] * width + REL_ARC_TO_SELF[true_card_owner][1],
                                         top + HAS_CARD_DICT[true_card_owner][1] * height + REL_ARC_TO_SELF[true_card_owner][2],
                                         REL_ARC_TO_SELF[true_card_owner][0], REL_ARC_TO_SELF[true_card_owner][0])
                pygame.draw.arc(screen, REL_COLOR_DICT[player.name], world_node, REL_ARC_TO_SELF[true_card_owner][3],
                                REL_ARC_TO_SELF[true_card_owner][4], 2)
            else:
                start_pos = (left + HAS_CARD_DICT[true_card_owner][0] * width, top + HAS_CARD_DICT[true_card_owner][1] * height)
                end_pos = (left + HAS_CARD_DICT[relation[0]][0] * width, top + HAS_CARD_DICT[relation[0]][1] * height)
                pygame.draw.line(screen, REL_COLOR_DICT[player.name], start_pos, end_pos, 2)




