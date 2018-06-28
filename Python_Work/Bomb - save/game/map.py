__author__ = 'BYSorynyos'

"""
Map manipulation class
"""

import pygame
from game import tile
from game import constants as c
from game import settings as s


class Map():
    # Attributes
    nr_maps = None
    map_x = None
    map_y = None
    map_tiles = [[]]
    map_bonuses = [[]]
    map_creatures = [[]]
    map_sprites = None

    def __init__(self):
        self.map_x = 14
        self.map_y = 14
        self.map_sprites = pygame.sprite.Group()
        self.map_tiles = [[100 for i in range(self.map_y)] for i in range(self.map_x)]
        self.map_bonuses = [[0 for i in range(self.map_y)] for i in range(self.map_x)]
        self.map_creatures = [[0 for i in range(self.map_y)] for i in range(self.map_x)]

    def clear_screen(self, scr):
        scr.fill(c.BLACK)

    def draw_map(self, scr):
        self.clear_screen(scr)
        for x in range(self.map_x):
            for y in range(self.map_y):
                new_tile = tile.Tile()
                new_tile.set_position(x * 70, y * 70)
                new_tile.set_image(self.map_tiles[x][y])
                self.map_sprites.add(new_tile)

        self.map_sprites.draw(scr)
        pygame.display.flip()

    def change_dimmensions(self, x, y):
        self.map_x = x
        self.map_y = y
        self.map_tiles = [[0 for i in range(y)] for i in range(x)]
        self.map_bonuses = [[0 for i in range(y)] for i in range(x)]
        self.map_creatures = [[0 for i in range(y)] for i in range(x)]

    def add_plcreature(self, x, y, val):
        if self.map_tiles[x][y] == 0 and self.map_creatures[x][y] == 0:
            self.map_creatures[x][y] = val

    def add_tile(self, x, y, val):
        if self.map_tiles[x][y] == 0 and self.map_creatures[x][y] == 0 and self.map_bonuses[x][y] == 0:
            self.map_tiles[x][y] = val

    def add_bonus(self, x, y, val):
        if self.map_tiles[x][y] != 0 and self.map_bonuses[x][y] == 0:
            self.map_bonuses[x][y] = val

    def load_map(self, map_number):
        with open(s.MAPS_PATH, 'r') as file:

            # number of maps
            line = file.readline()
            aux = line.strip("\n")
            nr = int(aux[0])
            self.nr_maps = nr

            for i in range(nr):

                if i == map_number:
                    break

                # x and y
                line = file.readline()
                aux = line.strip("\n")
                aux = aux.split(" ")
                self.change_dimmensions(int(aux[0]), int(aux[1]))

                # map_tiles
                for x in range(self.map_x):
                    line = file.readline()
                    aux = line.strip("\n")
                    aux = aux.split(" ")
                    for y in range(self.map_y):
                        self.map_tiles[x][y] = int(aux[y])

                # map_bonuses
                for x in range(self.map_x):
                    line = file.readline()
                    aux = line.strip("\n")
                    aux = aux.split(" ")
                    for y in range(self.map_y):
                        self.map_bonuses[x][y] = int(aux[y])

                # map_creatures
                for x in range(self.map_x):
                    line = file.readline()
                    aux = line.strip("\n")
                    aux = aux.split(" ")
                    for y in range(self.map_y):
                        self.map_creatures[x][y] = int(aux[y])

    def load_levels(self, level_number):
        with open(s.LEVELS_PATH, 'r') as file:

            # number of maps
            line = file.readline()
            aux = line.strip("\n")
            nr = int(aux[0])
            self.nr_maps = nr

            for i in range(nr):

                if i == level_number:
                    break

                # x and y
                line = file.readline()
                aux = line.strip("\n")
                aux = aux.split(" ")
                self.change_dimmensions(int(aux[0]), int(aux[1]))

                # map_tiles
                for x in range(self.map_x):
                    line = file.readline()
                    aux = line.strip("\n")
                    aux = aux.split(" ")
                    for y in range(self.map_y):
                        self.map_tiles[x][y] = int(aux[y])

                # map_bonuses
                for x in range(self.map_x):
                    line = file.readline()
                    aux = line.strip("\n")
                    aux = aux.split(" ")
                    for y in range(self.map_y):
                        self.map_bonuses[x][y] = int(aux[y])

                # map_creatures
                for x in range(self.map_x):
                    line = file.readline()
                    aux = line.strip("\n")
                    aux = aux.split(" ")
                    for y in range(self.map_y):
                        self.map_creatures[x][y] = int(aux[y])

    def save_map(self):
        file = open(s.MAPS_PATH, "w+")

        #rewrite the number of maps
        file.seek(0, 0)
        file.write(str(self.nr_maps + 1))

        # go to end
        file.seek(0, 2)
        file.write(str(self.map_x) + " ")
        file.write(str(self.map_y) + "/n")

        # map_tiles
        for x in range(self.map_x):
            for y in range(self.map_y - 1):
                file.write(str(self.map_tiles[x][y]) + " ")
            file.write(str(self.map_tiles[x][self.map_y]) + "/n")

        # map_bonuses
        for x in range(self.map_x):
            for y in range(self.map_y - 1):
                file.write(str(self.map_bonuses[x][y]) + " ")
            file.write(str(self.map_bonuses[x][self.map_y]) + "/n")

        # map_creatures
        for x in range(self.map_x):
            for y in range(self.map_y - 1):
                file.write(str(self.map_creatures[x][y]) + " ")
            file.write(str(self.map_creatures[x][self.map_y]) + "/n")

    def save_level(self):
        file = open(s.LEVELS_PATH, "w+")

        #rewrite the number of maps
        file.seek(0, 0)
        file.write(str(self.nr_maps + 1))

        # go to end
        file.seek(0, 2)
        file.write(str(self.map_x) + " ")
        file.write(str(self.map_y) + "/n")

        # map_tiles
        for x in range(self.map_x):
            for y in range(self.map_y - 1):
                file.write(str(self.map_tiles[x][y]) + " ")
            file.write(str(self.map_tiles[x][self.map_y]) + "/n")

        # map_bonuses
        for x in range(self.map_x):
            for y in range(self.map_y - 1):
                file.write(str(self.map_bonuses[x][y]) + " ")
            file.write(str(self.map_bonuses[x][self.map_y]) + "/n")

        # map_creatures
        for x in range(self.map_x):
            for y in range(self.map_y - 1):
                file.write(str(self.map_creatures[x][y]) + " ")
            file.write(str(self.map_creatures[x][self.map_y]) + "/n")