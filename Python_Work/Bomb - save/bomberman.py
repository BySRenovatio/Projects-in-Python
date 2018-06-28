__author__ = 'BYSorynyos'

'''
Main bomberman file
'''

from game import settings as s
from game import constants as c
from game import menu
from game import highscores
from game import map
from game import tile
from game import bonus
from game import enemy
from game import player

import pygame
import os


def main():
    """ Main program """

    pygame.init()

    # Set starting position of the window
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % s.SCREEN_START_POS

    # Set the height and width of the screen
    size = [s.SCREEN_WIDTH, s.SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(" Bomberman v.1.0 ")

    # Loop until player clicks a button
    done = False
    iamhere = "menu"
    iamhere_map = None

    new_menu = menu.Menu()
    new_menu.draw_menu(screen)

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # --- Main Program Loop ---
    while not done:
        all_events = pygame.event.get()
        for event in all_events:                                        # User did something
            if event.type == pygame.QUIT:                               # If user clicked close
                done = True                                             # Flag that we are done so we exit the loop

        # Display the menu
        if iamhere == "menu":
            new_menu = menu.Menu()
            new_menu.clear_screen(screen)
            new_menu.draw_menu(screen)

            for event in all_events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        done = True
                    elif event.type is pygame.K_c:
                        iamhere = "campaign"
                    elif event.key is pygame.K_l:
                        iamhere = "lan"
                    elif event.key is pygame.K_o:
                        iamhere = "how2play"
                    elif event.key is pygame.K_m:
                        iamhere = "map"
                        iamhere_map = "map"
                        current = 0
                    elif event.key is pygame.K_a:
                        iamhere = "achivements"
                    elif event.key is pygame.K_h:
                        iamhere = "highscores"
                    elif event.key is pygame.K_s:
                        iamhere = "settings"

        # Display the highscores
        if iamhere == "highscores":
            new_highscores = highscores.Highscores()
            new_highscores.clear_screen(screen)
            new_highscores.draw_highscores(screen)

            for event in all_events:
                if event.type == pygame.KEYDOWN:
                    if event.key is pygame.K_ESCAPE:
                        iamhere = "menu"

        # Display the map - editor
        if iamhere == "map":
            new_map = map.Map()

            if iamhere_map == "map":
                for event in all_events:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT and current > 0:
                            current -= 1
                            new_map.load_map(current)
                            new_map.draw_map(screen)
                            break
                        elif event.key == pygame.K_RIGHT:
                            current += 1
                            new_map.load_map(current)
                            new_map.draw_map(screen)
                            break
                        elif event.key == pygame.K_s:
                            new_map.save_map()
                            break
                        elif event.key == pygame.K_DOWN:
                            current = 0
                            iamhere_map = "levels"
                            break
                        elif event.key == pygame.K_ESCAPE:
                            iamhere = "menu"
                            break
                        else:
                            new_map.load_map(current)
                            new_map.draw_map(screen)
                            break
            elif iamhere_map == "levels":
                for event in all_events:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT and current > 0:
                            current -= 1
                            new_map.load_levels(current)
                            new_map.draw_map(screen)
                            break
                        elif event.key == pygame.K_RIGHT:
                            current += 1
                            new_map.load_levels(current)
                            new_map.draw_map(screen)
                            break
                        elif event.key == pygame.K_s:
                            new_map.save_level()
                            break
                        elif event.key == pygame.K_UP:
                            current = 0
                            iamhere_map = "map"
                            break
                        elif event.key == pygame.K_DOWN:
                            iamhere_map = "tiles"
                            current = c.TILE_0
                            break
                        elif event.key == pygame.K_ESCAPE:
                            iamhere = "menu"
                            break
                        else:
                            new_map.load_levels(current)
                            new_map.draw_map(screen)
                            break
            elif iamhere_map == "tiles":
                for event in all_events:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT and current > c.TILE_0:
                            current -= 1
                            new_tile = tile.Tile()
                            new_tile.set_position(c.TILE_POS_X, c.TILE_POS_Y)
                            new_tile.set_image(current)
                            one_tile = pygame.sprite.Group()
                            one_tile.add(new_tile)
                            one_tile.draw(screen)
                            pygame.display.flip()
                            break
                        elif event.key == pygame.K_RIGHT and current < c.TILE_NUMBER:
                            current += 1
                            new_tile = tile.Tile()
                            new_tile.set_position(c.TILE_POS_X, c.TILE_POS_Y)
                            new_tile.set_image(current)
                            one_tile = pygame.sprite.Group()
                            one_tile.add(new_tile)
                            one_tile.draw(screen)
                            pygame.display.flip()
                            break
                        elif event.key == pygame.K_UP:
                            current = 0
                            iamhere_map = "levels"
                            break
                        elif event.key == pygame.K_DOWN:
                            current = c.BONUS_0
                            iamhere_map = "bonus"
                            break
                        elif event.key == pygame.K_ESCAPE:
                            iamhere = "menu"
                            break
                        else:
                            new_tile = tile.Tile()
                            new_tile.set_position(c.TILE_POS_X, c.TILE_POS_Y)
                            new_tile.set_image(current)
                            one_tile = pygame.sprite.Group()
                            one_tile.add(new_tile)
                            one_tile.draw(screen)
                            pygame.display.flip()
                            break
            elif iamhere_map == "bonus":
                for event in all_events:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT and current > c.BONUS_0:
                            current -= 1
                            new_bonus = bonus.Bonus()
                            new_bonus.set_position(c.BONUS_POS_X, c.BONUS_POS_Y)
                            new_bonus.set_image(current)
                            one_bonus = pygame.sprite.Group()
                            one_bonus.add(new_bonus)
                            one_bonus.draw(screen)
                            pygame.display.flip()
                            break
                        elif event.key == pygame.K_RIGHT and current < c.BONUS_NUMBER:
                            current += 1
                            new_bonus = bonus.Bonus()
                            new_bonus.set_position(c.BONUS_POS_X, c.BONUS_POS_Y)
                            new_bonus.set_image(current)
                            one_bonus = pygame.sprite.Group()
                            one_bonus.add(new_bonus)
                            one_bonus.draw(screen)
                            pygame.display.flip()
                            break
                        elif event.key == pygame.K_UP:
                            iamhere_map = "tiles"
                            current = c.TILE_0
                            break
                        elif event.key == pygame.K_DOWN:
                            iamhere_map = "enemy"
                            current = c.ENEMY_0
                        elif event.key == pygame.K_ESCAPE:
                            iamhere = "menu"
                            break
                        else:
                            new_bonus = bonus.Bonus()
                            new_bonus.set_position(c.BONUS_POS_X, c.BONUS_POS_Y)
                            new_bonus.set_image(current)
                            one_bonus = pygame.sprite.Group()
                            one_bonus.add(new_bonus)
                            one_bonus.draw(screen)
                            pygame.display.flip()
                            break
            elif iamhere_map == "enemy":
                for event in all_events:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT and current > c.ENEMY_0:
                            current -= 1
                            new_enemy = enemy.Enemy()
                            new_enemy.set_position(c.ENEMY_POS_X, c.ENEMY_POS_Y)
                            new_enemy.set_image(current)
                            one_enemy = pygame.sprite.Group()
                            one_enemy.add(new_enemy)
                            one_enemy.draw(screen)
                            pygame.display.flip()
                            break
                        elif event.key == pygame.K_RIGHT and current < c.ENEMY_NUMBER:
                            current += 1
                            new_enemy = enemy.Enemy()
                            new_enemy.set_position(c.ENEMY_POS_X, c.ENEMY_POS_Y)
                            new_enemy.set_image(current)
                            one_enemy = pygame.sprite.Group()
                            one_enemy.add(new_enemy)
                            one_enemy.draw(screen)
                            pygame.display.flip()
                            break
                        elif event.key == pygame.K_UP:
                            iamhere_map = "bonus"
                            current = c.BONUS_0
                            break
                        elif event.key == pygame.K_DOWN:
                            iamhere_map = "player"
                            current = c.PLAYER_1
                            break
                        elif event.key == pygame.K_ESCAPE:
                            iamhere = "menu"
                            break
                        else:
                            new_enemy = enemy.Enemy()
                            new_enemy.set_position(c.ENEMY_POS_X, c.ENEMY_POS_Y)
                            new_enemy.set_image(current)
                            one_enemy = pygame.sprite.Group()
                            one_enemy.add(new_enemy)
                            one_enemy.draw(screen)
                            pygame.display.flip()
                            break
            elif iamhere_map == "player":
                for event in all_events:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT and current > c.PLAYER_1:
                            current -= 1
                            new_player = player.Player()
                            new_player.set_position(c.PLAYER_POS_X, c.PLAYER_POS_Y)
                            new_player.set_image(current)
                            one_player = pygame.sprite.Group()
                            one_player.add(new_player)
                            one_player.draw(screen)
                            pygame.display.flip()
                            break
                        elif event.type == pygame.K_RIGHT and current < c.PLAYER_3:
                            current += 1
                            new_player = player.Player()
                            new_player.set_position(c.PLAYER_POS_X, c.PLAYER_POS_Y)
                            new_player.set_image(current)
                            one_player = pygame.sprite.Group()
                            one_player.add(new_player)
                            one_player.draw(screen)
                            pygame.display.flip()
                            break
                        elif event.type == pygame.K_UP:
                            iamhere_map = "enemy"
                            current = c.ENEMY_0
                            break
                        elif event.key == pygame.K_ESCAPE:
                            iamhere = "menu"
                            break
                        else:
                            new_player = player.Player()
                            new_player.set_position(c.PLAYER_POS_X, c.PLAYER_POS_Y)
                            new_player.set_image(current)
                            one_player = pygame.sprite.Group()
                            one_player.add(new_player)
                            one_player.draw(screen)
                            pygame.display.flip()
                            break
        # Limit to the config file speed
        clock.tick(s.SPEED)

    # IDLE friendly ... no hang on exit
    pygame.quit()

if __name__ == "__main__":
    main()