__author__ = 'BYSorynyos'

"""
Constants definition
"""

from game import settings as s

# Color definition
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Define some constants
H_COORDS = ((s.SCREEN_WIDTH - 450) // 2, (s.SCREEN_HEIGHT - 800) // 2)
H_FONT = "Comic Sans MS"
H_SIZE_1 = 50
H_SIZE_2 = 40
H_SIZE_3 = 30

# Path to graphics/tiles
# Path to graphics/bonus
# Path to graphics/player
# Path to graphics/enemy
PATH_G_TILES = "graphics/tiles/"
PATH_G_BONUS = "graphics/bonus/"
PATH_G_PLAYER = "graphics/player/"
PATH_G_ENEMY = "graphics/enemy/"

# Path bomb
PATH_BOMB_0 = "graphics/bomb.png"
PATH_BOMB_1 = "graphics/bombFlash.png"

# Path star
PATH_STAR = "graphics/star.png"

# Player codes
PLAYER_1 = 1
PLAYER_1_S_0 = "p1_walkxx.png"
PLAYER_1_S_1 = "p1_duck.png"
PLAYER_1_S_2 = "p1_stand.png"

PLAYER_2 = 2
PLAYER_2_S_0 = "p2_walkxx.png"
PLAYER_2_S_1 = "p2_duck.png"
PLAYER_2_S_2 = "p2_stand.png"

PLAYER_3 = 3
PLAYER_3_S_0 = "p3_walkxx.png"
PLAYER_3_S_1 = "p3_duck.png"
PLAYER_3_S_2 = "p3_stand.png"

# Enemy codes
ENEMY_NUMBER = 33
ENEMY_0 = 10
ENEMY_0_S = "barnacle"
ENEMY_1 = 11
ENEMY_1_S = "bat"
ENEMY_2 = 12
ENEMY_2_S = "bee"
ENEMY_3 = 13
ENEMY_3_S = "fishGreen"
ENEMY_4 = 14
ENEMY_4_S = "fishPink"
ENEMY_5 = 15
ENEMY_5_S = "fly"
ENEMY_6 = 16
ENEMY_6_S = "frog"
ENEMY_7 = 17
ENEMY_7_S = "ghost"
ENEMY_8 = 18
ENEMY_8_S = "grassBlock"
ENEMY_9 = 19
ENEMY_9_S = "ladyBug"
ENEMY_10 = 20
ENEMY_10_S = "mouse"
ENEMY_11 = 21
ENEMY_11_S = "piranha"
ENEMY_12 = 22
ENEMY_12_S = "slime"
ENEMY_13 = 23
ENEMY_13_S = "slimeBlock"
ENEMY_14 = 24
ENEMY_14_S = "slimeBlue"
ENEMY_15 = 25
ENEMY_15_S = "slimeGreen"
ENEMY_16 = 26
ENEMY_16_S = "slimeWalk"
ENEMY_17 = 27
ENEMY_17_S = "snail_walk"
ENEMY_18 = 28
ENEMY_18_S = "snailWalk"
ENEMY_19 = 29
ENEMY_19_S = "snake"
ENEMY_20 = 30
ENEMY_20_S = "spider_walk"
ENEMY_21 = 31
ENEMY_21_S = "spinner"
ENEMY_22 = 32
ENEMY_22_S = "spinnerHalf"
ENEMY_23 = 33
ENEMY_23_S = "warm"

# Bonuses codes
BONUS_NUMBER = 61
BONUS_0 = 50
BONUS_0_S = "bombpass.png"
BONUS_1 = 51
BONUS_1_S = "bombs1.png"
BONUS_2 = 52
BONUS_2_S = "detonator.png"
BONUS_3 = 53
BONUS_3_S = "flamepass.png"
BONUS_4 = 54
BONUS_4_S = "intowall.png"
BONUS_5 = 55
BONUS_5_S = "invisible.png"
BONUS_6 = 56
BONUS_6_S = "life.png"
BONUS_7 = 57
BONUS_7_S = "points100.png"
BONUS_8 = 58
BONUS_8_S = "points1000.png"
BONUS_9 = 59
BONUS_9_S = "points10000.png"
BONUS_10 = 60
BONUS_10_S = "range1.png"
BONUS_11 = 61
BONUS_11_S = "speed.png"

# Tile codes
TILE_NUMBER = 134
TILE_0 = 100
TILE_0_S = "zero.png"
TILE_1 = 101
TILE_1_S = "boxAlt.png"
TILE_2 = 102
TILE_2_S = "boxCoin.png"
TILE_3 = 103
TILE_3_S = "boxCoin_disabled.png"
TILE_4 = 104
TILE_4_S = "boxCoinAlt.png"
TILE_5 = 105
TILE_5_S = "boxCoinAlt_disabled.png"
TILE_6 = 106
TILE_6_S = "boxEmpty.png"
TILE_7 = 107
TILE_7_S = "boxExplosive.png"
TILE_8 = 108
TILE_8_S = "boxExplosive_disabled"
TILE_9 = 109
TILE_9_S = "boxExplosiveAlt.png"
TILE_10 = 110
TILE_10_S = "boxItem.png"
TILE_11 = 111
TILE_11_S = "boxItem_disabled.png"
TILE_12 = 112
TILE_12_S = "boxItemAlt.png"
TILE_13 = 113
TILE_13_S = "boxItemAlt_disabled.png"
TILE_14 = 114
TILE_14_S = "boxWarning.png"
TILE_15 = 115
TILE_15_S = "brickWall.png"
TILE_16 = 116
TILE_16_S = "castle.png"
TILE_17 = 117
TILE_17_S = "castleCenter_rounded.png"
TILE_18 = 118
TILE_18_S = "dirt.png"
TILE_19 = 119
TILE_19_S = "grass.png"
TILE_20 = 120
TILE_20_S = "grassCenter_rounded.png"
TILE_21 = 121
TILE_21_S = "liquidLava.png"
TILE_22 = 122
TILE_22_S = "liquidWater.png"
TILE_23 = 123
TILE_23_S = "lock_blue.png"
TILE_24 = 124
TILE_24_S = "lock_green.png"
TILE_25 = 125
TILE_25_S = "lock_red.png"
TILE_26 = 126
TILE_26_S = "lock_yellow.png"
TILE_27 = 127
TILE_27_S = "sand.png"
TILE_28 = 128
TILE_28_S = "sandCenter_rounded.png"
TILE_29 = 129
TILE_29_S = "signExit.png"
TILE_30 = 130
TILE_30_S = "snowCenter_rounded.png"
TILE_31 = 131
TILE_31_S = "stone.png"
TILE_32 = 132
TILE_32_S = "stoneCenter_rounded.png"
TILE_33 = 133
TILE_33_S = "stoneWall.png"
TILE_34 = 134
TILE_34_S = "box.png"

# Tiles position
TILE_POS_X = 1500
TILE_POS_Y = 500

# Bonus position
BONUS_POS_X = 1500
BONUS_POS_Y = 500

# Enemy position
ENEMY_POS_X = 1500
ENEMY_POS_Y = 500

# Player position
PLAYER_POS_X = 1500
PLAYER_POS_Y = 500