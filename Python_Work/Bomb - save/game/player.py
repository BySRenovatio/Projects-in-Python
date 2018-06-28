__author__ = 'BYSorynyos'

"""
Bonus class
"""

import pygame
from game import constants as c


class Player(pygame.sprite.Sprite):
    # Attributes
    player_x = None
    player_y = None
    image = None
    rect = None

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

    def get_image(self, image_path):
        return pygame.image.load(c.PATH_G_PLAYER + image_path).convert()

    def set_position(self, x, y):
        self.player_x = x
        self.player_y = y

    def set_image(self, code):
        self.image = self.get_image(self.player_pathfromcode(code))
        self.image.set_colorkey(c.WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = self.player_x
        self.rect.y = self.player_y

    def player_pathfromcode(self, code):
        if code == c.PLAYER_1:
            return c.PLAYER_1_S_2
        elif code == c.PLAYER_2:
            return c.PLAYER_2_S_2
        elif code == c.PLAYER_3:
            return c.PLAYER_3_S_2