import os
import pygame


IMAGE_DICT = {
    'Diamonds'  : 'd',
    'Clubs'     : 'c',
    'Hearts'    : 'h',
    'Spades'    : 's',
    'seven'     : '7',
    'eight'     : '8',
    'nine'      : '9',
    'ten'       : 't',
    'jack'      : 'j',
    'queen'     : 'q',
    'king'      : 'k',
    'ace'       : 'a',
}

CENTER_POS = {
    'South' : (-50, 0),
    'West'  : (-100, -37.5),
    'North' : (-50, -75),
    'East'  : (0, -37.5),
}


def calc_rect(player, num_cards, screen_size):  #  Tim should use this calc_rect
    width = 75
    height = 100
    if player in ['South', 'North']:
        width += num_cards * 20
        left = screen_size[0]/2 - 20 * num_cards
        top = screen_size[1] * (1.0/4.0) - 100 if player == 'North' else screen_size[1] * (3.0/4.0)
    else:
        height += num_cards * 20
        top = screen_size[1]/2 - 20 * num_cards
        left = screen_size[0] * (1.0/6.0) - 75 if player == 'West' else screen_size[0] * (5.0/6.0)
    return left, top, width, height

def name_pos(player, num_cards, screen_size):
    left, top, width, height = calc_rect(player, num_cards, screen_size)
    if player == 'South':
        top += 100
    else:
        top -= 25
    return left, top

def calc_offset(player, num_cards, screen_size, idx):
    left, top, width, height = calc_rect(player, num_cards, screen_size)
    if player in ['South', 'North']:
        left += 20*idx
    else:
        top += 20*idx
    return left, top

def clear_hands(game_display, color, num_cards, screen_size):
    game_display.fill(color, pygame.Rect(calc_rect('South', num_cards, screen_size)))
    game_display.fill(color, pygame.Rect(calc_rect('North', num_cards, screen_size)))
    game_display.fill(color, pygame.Rect(calc_rect('East', num_cards, screen_size)))
    game_display.fill(color, pygame.Rect(calc_rect('West', num_cards, screen_size)))


def load_image(name, colorkey=None):
    fullname = os.path.join('img', name)

    try:
        image=pygame.image.load(fullname)
        image=image.convert()
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image, image.get_rect()
    except pygame.error:
        print('Cannot load image: ' +  str(name))
        raise SystemExit