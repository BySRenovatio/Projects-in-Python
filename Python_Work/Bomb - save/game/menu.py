__author__ = 'BYSorynyos'

"""
Contains the menu class
"""
import pygame
import operator
from game import constants as c
from game import settings as s

# Define some constants
MENU_COORDS = ((s.SCREEN_WIDTH - 450) // 2, (s.SCREEN_HEIGHT - 500) // 2)
MENU_FONT = "Comic Sans MS"
MENU_SIZE_1 = 50
MENU_SIZE_2 = 30


class Menu():
    # Attributes
    menu_coords = None
    menu_font = None

    def __init__(self):
        # Init the fonts
        pygame.font.init()
        self.menu_coords = MENU_COORDS
        self.menu_font = pygame.font.SysFont(MENU_FONT, MENU_SIZE_1, True)

    def draw_menu(self, screen):
        menu_label = self.menu_font.render("Bomberman Menu", 1, c.WHITE)
        screen.blit(menu_label, self.menu_coords)

        self.menu_coords = tuple(map(operator.add, self.menu_coords, (0, 100)))
        self.menu_font = pygame.font.SysFont(MENU_FONT, MENU_SIZE_2, True)
        menu_label = self.menu_font.render("(C)ampaign - Single Player", 1, c.WHITE)
        screen.blit(menu_label, self.menu_coords)

        self.menu_coords = tuple(map(operator.add, self.menu_coords, (0, 50)))
        self.menu_font = pygame.font.SysFont(MENU_FONT, MENU_SIZE_2, True)
        menu_label = self.menu_font.render("(L)an - Multiplayer", 1, c.WHITE)
        screen.blit(menu_label, self.menu_coords)

        self.menu_coords = tuple(map(operator.add, self.menu_coords, (0, 50)))
        self.menu_font = pygame.font.SysFont(MENU_FONT, MENU_SIZE_2, True)
        menu_label = self.menu_font.render("H(o)w to play", 1, c.WHITE)
        screen.blit(menu_label, self.menu_coords)

        self.menu_coords = tuple(map(operator.add, self.menu_coords, (0, 50)))
        self.menu_font = pygame.font.SysFont(MENU_FONT, MENU_SIZE_2, True)
        menu_label = self.menu_font.render("(M)ap - Design", 1, c.WHITE)
        screen.blit(menu_label, self.menu_coords)

        self.menu_coords = tuple(map(operator.add, self.menu_coords, (0, 50)))
        self.menu_font = pygame.font.SysFont(MENU_FONT, MENU_SIZE_2, True)
        menu_label = self.menu_font.render("(A)chivements", 1, c.WHITE)
        screen.blit(menu_label, self.menu_coords)

        self.menu_coords = tuple(map(operator.add, self.menu_coords, (0, 50)))
        self.menu_font = pygame.font.SysFont(MENU_FONT, MENU_SIZE_2, True)
        menu_label = self.menu_font.render("(H)ighscores", 1, c.WHITE)
        screen.blit(menu_label, self.menu_coords)

        self.menu_coords = tuple(map(operator.add, self.menu_coords, (0, 50)))
        self.menu_font = pygame.font.SysFont(MENU_FONT, MENU_SIZE_2, True)
        menu_label = self.menu_font.render("(S)ettings", 1, c.WHITE)
        screen.blit(menu_label, self.menu_coords)

        self.menu_coords = tuple(map(operator.add, self.menu_coords, (0, 50)))
        self.menu_font = pygame.font.SysFont(MENU_FONT, MENU_SIZE_2, True)
        menu_label = self.menu_font.render("(Q)uit", 1, c.WHITE)
        screen.blit(menu_label, self.menu_coords)

        pygame.display.flip()

    def clear_screen(self, screen):
        screen.fill(c.BLACK)