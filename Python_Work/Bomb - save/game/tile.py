__author__ = 'BYSorynyos'

"""
Tiles class
"""

import pygame
from game import constants as c


class Tile(pygame.sprite.Sprite):
    # Attributes
    tile_x = None
    tile_y = None
    image = None
    rect = None

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

    def get_image(self, image_path):
        return pygame.image.load(c.PATH_G_TILES + image_path).convert()

    def set_position(self, x, y):
        self.tile_x = x
        self.tile_y = y

    def set_image(self, code):
        self.image = self.get_image(self.tile_pathfromcode(code))
        self.image.set_colorkey(c.WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = self.tile_x
        self.rect.y = self.tile_y

    def tile_pathfromcode(self, code):
        if code == c.TILE_0:
            return c.TILE_0_S
        elif code == c.TILE_1:
            return c.TILE_1_S
        elif code == c.TILE_2:
            return c.TILE_2_S
        elif code == c.TILE_3:
            return c.TILE_3_S
        elif code == c.TILE_4:
            return c.TILE_4_S
        elif code == c.TILE_5:
            return c.TILE_5_S
        elif code == c.TILE_6:
            return c.TILE_6_S
        elif code == c.TILE_7:
            return c.TILE_7_S
        elif code == c.TILE_8:
            return c.TILE_8_S
        elif code == c.TILE_9:
            return c.TILE_9_S
        elif code == c.TILE_10:
            return c.TILE_10_S
        elif code == c.TILE_11:
            return c.TILE_11_S
        elif code == c.TILE_12:
            return c.TILE_12_S
        elif code == c.TILE_13:
            return c.TILE_13_S
        elif code == c.TILE_14:
            return c.TILE_14_S
        elif code == c.TILE_15:
            return c.TILE_15_S
        elif code == c.TILE_16:
            return c.TILE_16_S
        elif code == c.TILE_17:
            return c.TILE_17_S
        elif code == c.TILE_18:
            return c.TILE_18_S
        elif code == c.TILE_19:
            return c.TILE_19_S
        elif code == c.TILE_20:
            return c.TILE_20_S
        elif code == c.TILE_21:
            return c.TILE_21_S
        elif code == c.TILE_22:
            return c.TILE_22_S
        elif code == c.TILE_23:
            return c.TILE_23_S
        elif code == c.TILE_24:
            return c.TILE_24_S
        elif code == c.TILE_25:
            return c.TILE_25_S
        elif code == c.TILE_26:
            return c.TILE_26_S
        elif code == c.TILE_27:
            return c.TILE_27_S
        elif code == c.TILE_28:
            return c.TILE_28_S
        elif code == c.TILE_29:
            return c.TILE_29_S
        elif code == c.TILE_30:
            return c.TILE_30_S
        elif code == c.TILE_31:
            return c.TILE_31_S
        elif code == c.TILE_32:
            return c.TILE_32_S
        elif code == c.TILE_33:
            return c.TILE_33_S
        elif code == c.TILE_34:
            return c.TILE_34_S