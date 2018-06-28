__author__ = 'BYSorynyos'

"""
Contains the methods for highscores class
"""

import pygame
import operator
from game import constants as c
from game import settings as s


class Highscores():
    #Attributes
    h_coords = None
    h_font = None
    v_highscores = None

    def __init__(self):
        # Init the fonts
        pygame.font.init()
        self.h_coords = c.H_COORDS
        self.h_font = pygame.font.SysFont(c.H_FONT, c.H_SIZE_1, 1, True)
        self.v_highscores = self.get_highscores(s.HIGH_PATH)

    def draw_highscores(self, screen):
        h_label = self.h_font.render("Highscores", 1, c.WHITE)
        screen.blit(h_label, self.h_coords)

        current = 0

        while current <= 18 and current < (len(self.v_highscores) - 1):
            if current == 0:
                self.h_coords = tuple(map(operator.add, self.h_coords, (0, 70)))
                self.h_font = pygame.font.SysFont(c.H_FONT, c.H_SIZE_2, True)
            else:
                self.h_coords = tuple(map(operator.add, self.h_coords, (0, 60)))
                self.h_font = pygame.font.SysFont(c.H_FONT, c.H_SIZE_3, True)
            h_label = self.h_font.render(self.v_highscores[current] + " : " +
                                         self.v_highscores[current + 1], 1, c.WHITE)
            screen.blit(h_label, self.h_coords)
            current += 2

        pygame.display.flip()


    def clear_screen(self, screen):
        screen.fill(c.BLACK)

    def get_highscores(self, path):
        vector = []
        with open(path) as file:
            for line in file:
                aux = line.strip("\n")
                aux = aux.split(" ")
                for string in aux:
                    vector.append(string)
        return vector
