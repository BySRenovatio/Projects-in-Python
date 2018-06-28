__author__ = 'BYSorynyos'

"""
Bonus class
"""

import pygame
from game import constants as c


class Bonus(pygame.sprite.Sprite):
    # Attributes
    bonus_x = None
    bonus_y = None
    image = None
    rect = None

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

    def get_image(self, image_path):
        return pygame.image.load(c.PATH_G_BONUS + image_path).convert()

    def set_position(self, x, y):
        self.bonus_x = x
        self.bonus_y = y

    def set_image(self, code):
        self.image = self.get_image(self.tile_pathfromcode(code))
        self.image.set_colorkey(c.WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = self.bonus_x
        self.rect.y = self.bonus_y

    def bonus_pathfromcode(self, code):
        if code == c.BONUS_0:
            return c.BONUS_0_S
        elif code == c.BONUS_1:
            return c.BONUS_1_S
        elif code == c.BONUS_2:
            return c.BONUS_2_S
        elif code == c.BONUS_3:
            return c.BONUS_3_S
        elif code == c.BONUS_4:
            return c.BONUS_4_S
        elif code == c.BONUS_5:
            return c.BONUS_5_S
        elif code == c.BONUS_6:
            return c.BONUS_6_S
        elif code == c.BONUS_7:
            return c.BONUS_7_S
        elif code == c.BONUS_8:
            return c.BONUS_8_S
        elif code == c.BONUS_9:
            return c.BONUS_9_S
        elif code == c.BONUS_10:
            return c.BONUS_10_S
        elif code == c.BONUS_11:
            return c.BONUS_11_S