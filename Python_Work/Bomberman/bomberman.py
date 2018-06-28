__author__ = 'BYSorynyos'

import pygame
import os

from game import settings


def main():
    """
    Main program code
    """

    pygame.init()

    # Set starting position of the window
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % settings.SCREEN_START_POS

    # Set the height and width of the screen
    size = [settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT]

    # Get a link to the display -> screen
    screen = pygame.display.set_mode(size)

    # Set a proper title for the game
    pygame.display.set_caption(" Bomberman v.1.0 ")

    # Initialize the clock (counting the fps)
    clock = pygame.time.Clock()

    # While not done -> cycle
    done = False

    while not done:
        # Get all the events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True

        # Draw phase


        # Update the scree
        pygame.display.flip()

        clock.tick(settings.SPEED)

    # IDLE friendly ... no hang on exit
    pygame.quit()

if __name__ == "__main__":
    main()