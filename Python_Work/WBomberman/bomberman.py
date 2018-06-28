#############################################################
# One version of implementation for the Bomberman game
# by Sorin Ionut Bajenaru (Romania), 24-Mar 2014, Coursera
#
# An Introduction to Interactive Programming in Python
# by Joe Warren, Scott Rixner, John Greiner, Stephen Wong
#
# All sprites, music, sounds provided from :
# http://kenney.nl/ -> licensed under ->
# CC0 1.0 Universal (CC0 1.0)
# Public Domain Dedication
#############################################################

#############################################################
# You will know when i update the project
# based on this version numbers
VER = "1.1.0"
ver_date = "03.05. 2014"
#############################################################

#############################################################
# importing the usual libraries
import simplegui
import random
#############################################################

#############################################################
# global constants
TILE_SIZE = 35
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
TIMER_INTERVAL = 100 								# 10 FPS
############################################################
DISTRUCTABLE_TILE = 0								# -> 0; 18
UNDISTRUCTABLE_TILE = 0								# -> 0; 8
MAP_TILE = 7										# -> 0; 10
PLAYER_MODEL = 0									# -> 0; 2
ENEMY_MODEL = 0                                     # -> 60; 83
#############################################################

#############################################################
# all the data is stored here :
PREFIX = 'https://dl.dropboxusercontent.com/u/3381080/bomberman/'
#############################################################

############################################################
# load tiles in memory
backTilesSizes = [[70, 70], [70, 70], [70, 70], [70, 70],
                  [70, 70], [70, 70], [70, 70], [70, 70],
                  [70, 70], [70, 70], [70, 70]]
backTiles = []
for i in range(1, 12):
    backTiles.append(simplegui.load_image(PREFIX + 'background_' + str(i) + '.png'))
############################################################

############################################################
# load undistructable tiles in memory
unTilesSizes = [[70, 70], [70, 70], [70, 70], [70, 70],
                [70, 70], [70, 70], [70, 70], [70, 70], [70, 70]]
unTiles = []
for i in range(1, 10):
    unTiles.append(simplegui.load_image(PREFIX + 'undistructable_' + str(i) + '.png'))
###########################################################

############################################################
# load distructable tiles in memory
disTilesSizes = [[70, 70], [70, 70], [70, 70], [70, 70],
                 [70, 70], [70, 70], [70, 70], [70, 70],
                 [70, 70], [70, 70], [70, 70], [70, 70],
                 [70, 70], [70, 70], [70, 70], [70, 70],
                 [70, 70], [70, 70], [70, 70]]
disTiles = []
for i in range(1, 20):
    disTiles.append(simplegui.load_image(PREFIX + 'distructable_' + str(i) + '.png'))
###########################################################

###########################################################
# load players in memory
plPlayerSizes = [[[72, 97], [72, 97], [72, 97], [72, 97], [72, 97], [72, 97],
                  [72, 97], [72, 97], [72, 97], [72, 97], [72, 97]],
                 [[70, 94], [70, 94], [70, 94], [70, 94], [70, 94], [70, 94],
                  [70, 94], [70, 94], [70, 94], [70, 94], [70, 94]],
                 [[72, 97], [72, 97], [72, 97], [72, 97], [72, 97], [72, 97],
                  [72, 97], [72, 97], [72, 97], [72, 97], [72, 97]]]
plPlayer = []
for i in range(3):
    plPlayer.append([])
for i in range(3):
    for j in range(1, 12):
        plPlayer[i].append(simplegui.load_image(PREFIX + 'p' + str(i+1) + '_walk' + str(j) + '.png'))
###########################################################

###########################################################
# load bomb into memory and fire
bmBombSize = [70, 70]
fFireSize = [70, 70]
bmBomb = []
fFire = []
bmBomb.append(simplegui.load_image(PREFIX + 'zbomb_1.png'))
bmBomb.append(simplegui.load_image(PREFIX + 'zbomb_2.png'))
fFire.append(simplegui.load_image(PREFIX + 'zfire.png'))
############################################################
# load enemies in memory
enEnemySizes = [[[51, 57], [51, 58], [51, 57], [51, 57]],
                [[70, 47], [88, 37], [70, 47], [70, 47]],
                [[56, 48], [61, 42], [56, 48], [56, 48]],
                [[60, 45], [57, 44], [60, 45], [57, 44]],
                [[60, 45], [57, 44], [60, 45], [57, 44]],
                [[57, 45], [65, 39], [57, 45], [57, 45]],
                [[58, 39], [61, 54], [61, 54], [61, 54]],
                [[51, 73], [51, 73], [51, 73], [51, 73]],
                [[71, 70], [71, 70], [71, 70], [71, 70]],
                [[58, 34], [59, 42], [61, 34], [58, 34]],
                [[59, 35], [58, 35], [59, 35], [59, 35]],
                [[45, 60], [45, 60], [45, 60], [45, 60]],
                [[49, 34], [57, 30], [49, 34], [49, 34]],
                [[63, 23], [63, 23], [63, 23], [63, 23]],
                [[51, 50], [51, 50], [51, 50], [51, 50]],
                [[63, 23], [63, 23], [63, 23], [63, 23]],
                [[49, 34], [57, 30], [49, 34], [49, 34]],
                [[49, 34], [57, 30], [49, 34], [49, 34]],
                [[50, 28], [51, 26], [59, 12], [57, 13]],
                [[60, 40], [55, 40], [43, 35], [55, 40]],
                [[54, 31], [57, 31], [44, 30], [44, 30]],
                [[72, 51], [77, 53], [69, 51], [71, 45]],
                [[63, 62], [61, 61], [63, 62], [61, 61]],
                [[63, 31], [61, 30], [63, 31], [61, 30]]]
enEnemy = []
for i in range(24):
    enEnemy.append([])
for i in range(24):
    for j in range(1, 5):
        enEnemy[i].append(simplegui.load_image(PREFIX + 'enemy_' + str(i+1) + '_' + str(j) + '.png'))
############################################################

###########################################################
# player class
PLAYER = None
###########################################################

###########################################################
# enemies vector
ENEMIES = []
############################################################

############################################################
# bombs vector
BOMBS = []
############################################################

############################################################
FLAMES = []
###########################################################

###########################################################
# create the first maps
# 0 -> 10 background tile
# 20 -> 28 undistructable tiles
# 30 -> 49 distructable tiles
# 60 -> 83 monsters
# 99, 98, 97 player models
# 3167 ->> 31 represents the bonus

current_map = [[0 for x in range(30)] for y in range(30)]
bonus_map = [[0 for x in range(30)] for y in range(30)]
MP_11_X = 20
MP_11_Y = 20
MP_11 = [[20,   20,   20,   20,   20,   20,   20,   20,   20,   20,   20,   20,   20,   20,   20,   20,   20,   20,   20,   20],
         [20,    0,    0,    0,    0,   31,    0,    0,    0,   20,   20,    0,    0,    0,    0,   31,    0,    0,    0,   20],
         [20,    0,    0,   31,    0,    0,    0,   31,    0,   20,   20,    0,    0,   31,    0,    0,    0,   31,    0,   20],
         [20,    0,   31,   31,    0,   31,   31,    0,    0,   20,   20,    0,   31,   31,    0,   31,   31,    0,    0,   20],
         [20,    0,    0,   31,    0,    0,    0,   31,    0,   20,   20,    0,    0,   31,    0,    0,    0,   31,    0,   20],
         [20,    0,   31,   31,    0,    0,   31,    0,    0,    0,   20,    0,   31,   31,    0,    0,   31,    0,    0,   20],
         [20,    0,    0,   31,    0,   31,    0,    0,    0,    0,    0,    0,    0,   31,    0,   31,    0,    0,    0,   20],
         [20,    0,   31,   31,    0,   31,    0,   31,    0,    0,    0,    0,   31,   31,    0,   31,    0,   31,    0,   20],
         [20,    0,    0,   31,    0,    0,    0,   31,    0,    0,    0,    0,    0,   31,    0,    0,    0,   31,    0,   20],
         [20,   20,   20,   20,   20,   20,   20,   20,   20,    0,    0,    0,   20,   20,   20,   20,   20,   20,   20,   20],
         [20,   20,   20,   20,   20,   20,   20,   20,   20,    0,   98,    0,   20,   20,   20,   20,   20,   20,   20,   20],
         [20,    0,    0,    0,    0,   31,    0,    0,    0,    0,    0,    0,    0,    0,    0,   31,    0,    0,    0,   20],
         [20,    0,    0,   31,    0,    0,    0,   31,    0,    0,    0,    0,    0,   31,    0,    0,    0,   31,    0,   20],
         [20,    0,   31,   31,    0,   31,   31,    0,    0,   20,   20,    0,   31,   31,    0,   31,   31,    0,    0,   20],
         [20,    0,    0,   31,    0,    0,    0,   31,    0,   20,   20,    0,    0,   31,    0,    0,    0,   31,    0,   20],
         [20,    0,   31,   31,    0,    0,   31,    0,    0,    0,   20,    0,   31,   31,    0,    0,   31,    0,    0,   20],
         [20,    0,    0,   31,    0,   31,    0,    0,    0,    0,    0,    0,    0,   31,    0,   31,    0,    0,    0,   20],
         [20,    0,   31,   31,    0,   31,    0,   31,    0,    0,    0,    0,   31,   31,    0,   31,    0,   31,    0,   20],
         [20,    0,    0,   31,    0,    0,    0,   31,    0,    0,    0,    0,    0,   31,    0,    0,    0,    0,    0,   20],
         [20,   20,   20,   20,   20,   20,   20,   20,   20,   20,   20,   20,   20,   20,   20,   20,   20,   20,   20,   20]]
###########################################################

############################################################
class Tile:
    def __init__(self, tile_position, tile_size, tile_type):
        self.x = tile_position[0]
        self.y = tile_position[1]
        self.w = tile_size[0]
        self.h = tile_size[1]
        self.tImage = tile_type

    def draw(self, canvas):
        canvas.draw_image(self.tImage, (self.w/2, self.h/2), (self.w, self.h), (self.x + self.w/4, self.y + self.h/4), (self.w/2, self.h/2))
#############################################################

#############################################################
class Enemy:
    def __init__(self, enemy_pos, enemy_type):
        self.x = enemy_pos[0]
        self.y = enemy_pos[1]
        self.etype = enemy_type
        self.imageIndex = 0
        self.w = enEnemySizes[enemy_type][0][0]
        self.h = enEnemySizes[enemy_type][0][1]
        self.eImage = enEnemy[enemy_type][0]
        self.dead = False
        self.counter = 30

    def update_image(self):
        self.imageIndex += 1
        if self.imageIndex == 2:
            self.imageIndex = 0
        self.w = enEnemySizes[self.etype][self.imageIndex][0]
        self.h = enEnemySizes[self.etype][self.imageIndex][1]
        self.eImage = enEnemy[self.etype][self.imageIndex]

    def update_image_dead(self):
        self.imageIndex += 1
        self.counter -= 1
        if self.imageIndex == 4:
            self.imageIndex = 2
        self.w = enEnemySizes[self.etype][self.imageIndex][0]
        self.h = enEnemySizes[self.etype][self.imageIndex][1]
        self.eImage = enEnemy[self.etype][self.imageIndex]

    def draw(self, canvas):
        canvas.draw_image(self.eImage, (self.w/2, self.h/2), (self.w, self.h), (self.x + self.w/8, self.y + self.h/8), (self.w/2, self.h/2))

    def set_dead(self):
        self.dead = True

    def howDead(self):
        return self.counter

    def isDead(self):
        return  self.dead

    def can_move(self, x, y):
        # get the tile number
        tile_x = x / TILE_SIZE
        tile_y = y / TILE_SIZE
        if 0 <= current_map[tile_y][tile_x] <= 10:
            return 1
        return 0

    def return_location(self):
        return [self.x / 35, self.y / 35]

    def move(self):
        player_coords = PLAYER.return_position()

        shall_we_move = random.randrange(0, 2)
        if shall_we_move == 0:
            return

        chance = random.randrange(0, 101)
        if chance > 2 * (self.etype + 2):
            return

        if player_coords[0] - self.x > 20:
            if self.can_move(self.x + 35, self.y) == 1:
                self.x += 35
                return
        if self.x - player_coords[0] > 20:
            if self.can_move(self.x - 35, self.y) == 1:
                self.x -= 35
                return
        if player_coords[1] - self.y > 20:
            if self.can_move(self.x, self.y + 35) == 1:
                self.y += 35
                return
        if self.y - player_coords[1] > 20:
            if self.can_move(self.x, self.y - 35) == 1:
                self.y -= 35
                return
#############################################################

#############################################################
class Player:
    def __init__(self, player_pos, player_type):
        self.x = player_pos[0]
        self.y = player_pos[1]
        self.ptype = player_type
        self.imageindex = 0
        self.w = plPlayerSizes[player_type][0][0]
        self.h = plPlayerSizes[player_type][0][1]
        self.pImage = plPlayer[player_type][0]
        self.speed = 1
        self.fire = 1
        self.bombs = 1
        self.life = 36
        self.allowed = True
        self.moving = 0
        self.moved = 0
    
    def update_model(self, val):
        self.ptype = val
    
    def return_position(self):
        return [self.x, self.y]

    def return_range(self):
        return self.fire

    def update_image(self):
        self.imageindex += 1
        if self.imageindex == 11:
            self.imageindex = 0
        self.w = plPlayerSizes[self.ptype][self.imageindex][0]
        self.h = plPlayerSizes[self.ptype][self.imageindex][1]
        self.pImage = plPlayer[self.ptype][self.imageindex]

        self.moving += 1
        if self.moving > 10:
            self.allowed = True
            self.moved = 0
            self.moving = 0

        if self.moved == self.speed:
            self.allowed = False

    def number_bombs(self):
        return self.bombs

    def can_move(self, x, y):
        # get the tile number
        tile_x = x / TILE_SIZE
        tile_y = y / TILE_SIZE
        if 0 <= current_map[tile_y][tile_x] <= 10 and self.allowed == True:
            self.moved += 1
            return 1
        return 0

    def move(self, x_axis, y_axis):
        if self.can_move(self.x + x_axis * 35, self.y + y_axis * 35) == 1:
            self.x += 35 * x_axis
            self.y += 35 * y_axis

    def got_bombs(self):
        self.bombs += 1
    
    def got_bombsd(self):
        self.bombs -= 1
        
    def get_bombs(self):
        return str(self.bombs)

    def got_speed(self):
        self.speed += 1
        
    def got_speedd(self):
        self.speed -= 1
        
    def get_speeds(self):
        return str(self.speed)
    
    def got_fire(self):
        self.fire += 1
    
    def got_fired(self):
        self.fire -= 1
        
    def get_fires(self):
        return str(self.fire)

    def got_life(self):
        self.life += 1

    def reset_bonus(self):
        self.fire = 1
        self.speed = 1
        self.bombs = 1
        self.life -= 1
        label1.set_text('Speed = ' + PLAYER.get_speeds())
        label2.set_text('Fire = ' + PLAYER.get_fires())
        label3.set_text('Bombs = ' + PLAYER.get_bombs())

    def draw(self, canvas):
        canvas.draw_image(self.pImage, (self.w/2, self.h/2), (self.w, self.h), (self.x + self.w/8, self.y + self.h/8), (self.w/2, self.h/2))
#############################################################

#############################################################
class Bomb:
    def __init__(self, bomb_position, bomb_size, bomb_range):
        self.x = bomb_position[0] - 8
        self.y = bomb_position[1] - 6
        self.w = bomb_size[0]
        self.h = bomb_size[1]
        self.bImage = bmBomb[0]
        self.fImage = fFire[0]
        self.fw = fFireSize[0]
        self.fh = fFireSize[1]
        self.imgIndex = 0
        self.active = True
        self.timer = 25
        self.range = bomb_range

        self.right = 0
        self.left = 0
        self.up = 0
        self.down = 0

        location_x = self.x / 35 + 1
        location_y = self.y / 35 + 1

        i = 1
        while current_map[location_y + i][location_x] <= 10:
            self.down += 1
            i += 1
        if 30 <= current_map[location_y + i][location_x] <= 49:
            self.down += 1

        i = 1
        while current_map[location_y][location_x + i] <= 10:
            self.right += 1
            i += 1
        if 30 <= current_map[location_y][location_x + i] <= 49:
            self.right += 1

        i = 1
        while current_map[location_y - i][location_x] <= 10:
            self.up += 1
            i += 1
        if 30 <= current_map[location_y - i][location_x] <= 49:
            self.up += 1

        i = 1
        while current_map[location_y][location_x - i] <= 10:
            self.left += 1
            i += 1
        if 30 <= current_map[location_y][location_x - i] <= 49:
            self.left += 1

    def draw_flames(self, canvas):
        loc_x = self.x / 35 + 1
        loc_y = self.y / 35 + 1

        for i in range(1, self.range + 1):
            if i <= self.right:
                canvas.draw_image(self.fImage, (self.fw/2, self.fh/2), (self.fw, self.fh), (self.x + (i * 35) + self.fw/4, self.y + self.fh/4), (self.fw, self.fh))
                FLAMES.append([loc_x + i, loc_y])

            if i <= self.down:
                canvas.draw_image(self.fImage, (self.fw/2, self.fh/2), (self.fw, self.fh), (self.x + self.fw/4, self.y + (i * 35) + self.fh/4), (self.fw, self.fh))
                FLAMES.append([loc_x, loc_y + i])

            if i <= self.left:
                canvas.draw_image(self.fImage, (self.fw/2, self.fh/2), (self.fw, self.fh), (self.x + (-i * 35) + self.fw/4, self.y + self.fh/4), (self.fw, self.fh))
                FLAMES.append([loc_x - i, loc_y])

            if i <= self.up:
                canvas.draw_image(self.fImage, (self.fw/2, self.fh/2), (self.fw, self.fh), (self.x + self.fw/4, self.y + (-i * 35) + self.fh/4), (self.fw, self.fh))
                FLAMES.append([loc_x, loc_y - i])

    def draw(self, canvas):
        if self.timer < 5:
            self.draw_flames(canvas)
        else:
            canvas.draw_image(self.bImage, (self.w/2, self.h/2), (self.w, self.h), (self.x + self.w/4, self.y + self.h/4), (self.w/2, self.h/2))

    def update_image(self):
        self.imgIndex += 1
        self.timer -= 1
        if self.imgIndex == 2:
            self.imgIndex = 0
        self.bImage = bmBomb[self.imgIndex]

        if self.timer == 0:
            self.active = False

    def bomb_active(self):
        return self.active
#############################################################


def draw_map(canvas):
    for x in range(MP_11_X):
        for y in range(MP_11_Y):
            if 0 <= current_map[x][y] <= 10:
                MAP_TILE = current_map[x][y]
                newTile = Tile((y*TILE_SIZE, x*TILE_SIZE), backTilesSizes[MAP_TILE], backTiles[MAP_TILE])
                newTile.draw(canvas)

def draw_bombs(canvas):
    for bmb in BOMBS:
        if bmb.bomb_active() == False:
            BOMBS.remove(bmb)
        else:
            bmb.draw(canvas)

def draw_undistructable(canvas):
     for x in range(MP_11_X):
        for y in range(MP_11_Y):
            if 20 <= current_map[x][y] <= 28:
                UNDISTRUCTABLE_TILE = current_map[x][y] - 20
                newTile = Tile((y*TILE_SIZE, x*TILE_SIZE), unTilesSizes[UNDISTRUCTABLE_TILE], unTiles[UNDISTRUCTABLE_TILE])
                newTile.draw(canvas)

def draw_distructable(canvas):
    for x in range(MP_11_X):
        for y in range(MP_11_Y):
            if 30 <= current_map[x][y] <= 48:
                DISTRUCTABLE_TILE = current_map[x][y] - 30
                newTile = Tile((y*TILE_SIZE, x*TILE_SIZE), disTilesSizes[DISTRUCTABLE_TILE], disTiles[DISTRUCTABLE_TILE])
                newTile.draw(canvas)

def draw_player(canvas):
    PLAYER.draw(canvas)

def draw_enemies(canvas):
    for i in range(len(ENEMIES)):
        ENEMIES[i].draw(canvas)

def draw_handler(canvas):
  draw_map(canvas)
  draw_undistructable(canvas)
  draw_distructable(canvas)
  draw_player(canvas)
  draw_enemies(canvas)
  draw_bombs(canvas)

def moving_objects():
    global PLAYER
    global ENEMIES
    global FLAMES
    trENEMIES = []

    # change pictures in player
    PLAYER.update_image()

    # change enemies pictures + move them
    del trENEMIES[:]
    for i in range(len(ENEMIES)):
        if ENEMIES[i].isDead() == False:
            ENEMIES[i].update_image()
            ENEMIES[i].move()
        else:
            if ENEMIES[i].howDead() > 0:
                ENEMIES[i].update_image_dead()
            else:
                trENEMIES.append(ENEMIES[i])

    for ene in trENEMIES:
        ENEMIES.remove(ene)

    for i in range(len(BOMBS)):
        BOMBS[i].update_image()

    for coords in FLAMES:
        if 30 <= current_map[coords[1]][coords[0]] <= 49:
            current_map[coords[1]][coords[0]] = MAP_TILE

        for i in range(len(ENEMIES)):
            ene = ENEMIES[i]
            location = ene.return_location()
            if location[0] == coords[0] and location[1] == coords[1]:
                ENEMIES[i].set_dead()

        location = PLAYER.return_position()
        if location[0] / 35 == coords[0] and location[1] / 35 == coords[1]:
            PLAYER.reset_bonus()

    del FLAMES[:]

    for ene in ENEMIES:
        location = ene.return_location()
        plocation = PLAYER.return_position()
        if location[0] == plocation[0] / 35 and location[1] == plocation[1] / 35:
            PLAYER.reset_bonus()
            ENEMIES.remove(ene)

def keydown(key):
    global PLAYER

    if key == simplegui.KEY_MAP['right']:
        PLAYER.move(1, 0)
    elif key == simplegui.KEY_MAP['left']:
        PLAYER.move(-1, 0)
    elif key == simplegui.KEY_MAP['up']:
        PLAYER.move(0, -1)
    elif key == simplegui.KEY_MAP['down']:
        PLAYER.move(0, 1)
    elif key == simplegui.KEY_MAP['space']:
        if len(BOMBS) < PLAYER.number_bombs():
            new_bomb = Bomb(PLAYER.return_position(), bmBombSize, PLAYER.return_range())
            BOMBS.append(new_bomb)

def inits():
    global PLAYER
    
    global lastUpdated
    lastUpdated = 0
    
    # 0 -> 10 background tile
    # 20 -> 28 undistructable tiles
    # 30 -> 49 distructable tiles
    # 60 -> 83 monsters
    # 99, 98, 97 player models
    # 3167 ->> 31 represents the bonus

    for x in range(MP_11_X):
        for y in range(MP_11_Y):
            current_map[x][y] = MP_11[x][y]
            # player zone
            if 97 <= current_map[x][y] <= 99:
                PLAYER_MODEL = current_map[x][y] - 97
                PLAYER = Player((y*TILE_SIZE+7, x*TILE_SIZE), PLAYER_MODEL)
                current_map[x][y] = 0
            if 60 <= current_map[x][y] <= 83:
                ENEMY_MODEL = current_map[x][y] - 60
                ENEMIES.append(Enemy((y*TILE_SIZE+10, x*TILE_SIZE+5), ENEMY_MODEL))
                current_map[x][y] = 0

def button_speed():
    global PLAYER
    PLAYER.got_speed()
    label1.set_text('Speed = ' + PLAYER.get_speeds())

def button_speedd():
    global PLAYER
    PLAYER.got_speedd()
    label1.set_text('Speed = ' + PLAYER.get_speeds())
    
def button_fire():
    global PLAYER
    PLAYER.got_fire()
    label2.set_text('Fire = ' + PLAYER.get_fires())
    
def button_fired():
    global PLAYER
    PLAYER.got_fired()
    label2.set_text('Fire = ' + PLAYER.get_fires())
    
def button_bombs():
    global PLAYER
    PLAYER.got_bombs()
    label3.set_text('Bombs = ' + PLAYER.get_bombs())
    
def button_bombsd():
    global PLAYER
    PLAYER.got_bombsd()
    label3.set_text('Bombs = ' + PLAYER.get_bombs())
    
def input_enemy(inp):
    global ENEMY_MODEL
    global lastUpdated
    
    try: 
        val = int(inp)
    except:
        print "Non int value inserted!"
        
    if 1 <= val <= 24:
        val -= 1
        ENEMY_MODEL = val
        lastUpdated = 1
    else:
        return
    
def input_background(inp):
    global MAP_TILE
    global lastUpdated
    
    try: 
        val = int(inp)
    except:
        print "Non int value inserted!"
        
    if 1 <= val <= 11:
        val -= 1
        MAP_TILE = val
        lastUpdated = 2
    else:
        return
    
def input_distructable(inp):
    global DISTRUCTABLE_TILE
    global lastUpdated
    
    try: 
        val = int(inp)
    except:
        print "Non int value inserted!"
        
    if 1 <= val <= 19:
        val += 29
        DISTRUCTABLE_TILE = val
        lastUpdated = 3
    else:
        lastUpdated = 0
        return
    
def input_indistructable(inp):
    global UNDISTRUCTABLE_TILE
    global lastUpdated 
    
    try: 
        val = int(inp)
    except:
        print "Non int value inserted!"
        
    if 1 <= val <= 9:
        val += 19
        UNDISTRUCTABLE_TILE = val
        lastUpdated = 4
    else:
        lastUpdated = 0
        return
    
def input_player(inp):  
    global PLAYER
    
    try:
        val = int(inp)
    except:
        print "Non int value inserted!"
        
    if 1 <= val <= 3:
        val -= 1
        PLAYER.update_model(val)
    else:
        return
    
def mouse_handler(pos):
    global ENEMIES
    global lastUpdated
    
    x = pos[0] // 35
    y = pos[1] // 35
    
    if lastUpdated == 1:			# enemy
        ENEMIES.append(Enemy((x*TILE_SIZE+10, y*TILE_SIZE+5), ENEMY_MODEL))
        lastUpdated = 0
    elif lastUpdated == 2:			# background
        current_map[y][x] = MAP_TILE
    elif lastUpdated == 3:			# distructable
        current_map[y][x] = DISTRUCTABLE_TILE
    elif lastUpdated == 4:			# indistructable
        current_map[y][x] = UNDISTRUCTABLE_TILE      
        
# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame('Bomberman : ' + VER, SCREEN_WIDTH, SCREEN_HEIGHT)

frame.set_draw_handler(draw_handler)
frame.set_keydown_handler(keydown)
frame.set_mouseclick_handler(mouse_handler)

leTimer = simplegui.create_timer(TIMER_INTERVAL, moving_objects)
leTimer.start()

button1 = frame.add_button('Inc Speed', button_speed, 150)
label1 = frame.add_label('Speed = 1')
button2 = frame.add_button('Dec Speed', button_speedd, 150)

label11 = frame.add_label(' ')

button3 = frame.add_button('Inc Fire Range', button_fire, 150)
label2 = frame.add_label('Fire = 1')
button4 = frame.add_button('Dec Fire Range', button_fired, 150)

label12 = frame.add_label(' ')

button5 = frame.add_button('Inc Bomb Number', button_bombs, 150)
label3 = frame.add_label('Bombs = 1')
button6 = frame.add_button('Dec Bomb Number', button_bombsd, 150)

label13 = frame.add_label(' ')
inp1 = frame.add_input('Enemy Model [1 - 24]', input_enemy, 150)

label14 = frame.add_label(' ')
inp2 = frame.add_input('Background Model [1 - 11]', input_background, 150)

label15 = frame.add_label(' ')
inp3 = frame.add_input('Dis Tile Model [1 - 19]', input_distructable, 150)

label16 = frame.add_label(' ')
inp4 = frame.add_input('Indis Tile Model [1 - 9]', input_indistructable, 150)

label17 = frame.add_label(' ')
inp5 = frame.add_input('Player Model [1 - 3]', input_player, 150)

# Start the frame animation
inits()
frame.start()