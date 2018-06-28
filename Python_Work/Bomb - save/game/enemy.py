__author__ = 'BYSorynyos'

"""
Bonus class
"""

import pygame
from game import constants as c

# Constants for the enemy name
NAME_1 = "_0.png"
NAME_2 = "_1.png"
DEAD_1 = "_dead_0.png"
DEAD_2 = "_dead_1.png"


class Enemy(pygame.sprite.Sprite):
    # Attributes
    enemy_x = None
    enemy_y = None
    image = None
    rect = None

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

    def get_image(self, image_path):
        return pygame.image.load(c.PATH_G_ENEMY + image_path).convert()

    def set_position(self, x, y):
        self.enemy_x = x
        self.enemy_y = y

    def set_image(self, code):
        self.image = self.get_image(self.enemy_pathfromcode(code))
        self.image.set_colorkey(c.WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = self.enemy_x
        self.rect.y = self.enemy_y

    def enemy_pathfromcode(self, code):
        if code == c.ENEMY_0:
            return c.ENEMY_0_S + NAME_1
        elif code == c.ENEMY_1:
            return c.ENEMY_1_S + NAME_1
        elif code == c.ENEMY_2:
            return c.ENEMY_2_S + NAME_1
        elif code == c.ENEMY_3:
            return c.ENEMY_3_S + NAME_1
        elif code == c.ENEMY_4:
            return c.ENEMY_4_S + NAME_1
        elif code == c.ENEMY_5:
            return c.ENEMY_5_S + NAME_1
        elif code == c.ENEMY_6:
            return c.ENEMY_6_S + NAME_1
        elif code == c.ENEMY_7:
            return c.ENEMY_7_S + NAME_1
        elif code == c.ENEMY_8:
            return c.ENEMY_8_S + NAME_1
        elif code == c.ENEMY_9:
            return c.ENEMY_9_S + NAME_1
        elif code == c.ENEMY_10:
            return c.ENEMY_10_S + NAME_1
        elif code == c.ENEMY_11:
            return c.ENEMY_11_S + NAME_1
        elif code == c.ENEMY_12:
            return c.ENEMY_12_S + NAME_1
        elif code == c.ENEMY_13:
            return c.ENEMY_13_S + NAME_1
        elif code == c.ENEMY_14:
            return c.ENEMY_14_S + NAME_1
        elif code == c.ENEMY_15:
            return c.ENEMY_15_S + NAME_1
        elif code == c.ENEMY_16:
            return c.ENEMY_16_S + NAME_1
        elif code == c.ENEMY_17:
            return c.ENEMY_17_S + NAME_1
        elif code == c.ENEMY_18:
            return c.ENEMY_18_S + NAME_1
        elif code == c.ENEMY_19:
            return c.ENEMY_19_S + NAME_1
        elif code == c.ENEMY_20:
            return c.ENEMY_20_S + NAME_1
        elif code == c.ENEMY_21:
            return c.ENEMY_21_S + NAME_1
        elif code == c.ENEMY_22:
            return c.ENEMY_22_S + NAME_1
        elif code == c.ENEMY_23:
            return c.ENEMY_23_S + NAME_1