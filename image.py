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