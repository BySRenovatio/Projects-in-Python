import random

INTERVAL = 20                           # 50 FPS

VER = "1.0.1"
DATE = "07/05/2014"

try:
    import simplegui
except:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

class Tile:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.val = value
        self.alive = True
        self.dir = [0, 0]

    def column(self):
        return self.y

    def value(self):
        return self.val

    def row(self):
        return self.x

    def direction(self):
        return self.dir

    def isAlive(self):
        return self.alive

    def double(self):
        self.val += self.val

    def reset(self):
        self.val = 0

    def __str__(self):
        s = "[" + str(self.x) + "," + str(self.y) + "]" + " value = " + str(self.val) + " -> " + str(self.alive)
        return s

    def update(self, valu):
        self.val = valu

    def moveLeft(self, ltiles):
        if self.alive is False:
            return False

        for x in range(5):
            for y in range(4):
                tile = ltiles[x][y]
                if tile.row() == self.x:                                                                                    # same row
                    if tile.column() == self.y - 1 and self.y - 1 >= 0 and tile.value() == self.val and self.val > 0:       # tile on the left
                        self.val *= 2
                        self.dir = [0, -1]
                        self.alive = False
                        return False
                    if tile.column() == self.y - 1 and self.y - 1 >= 0 and tile.value() == 0:
                        self.y -= 1
                        return True
        return False

    def moveRight(self, ltiles):
        if self.alive is False:
            return False

        for x in range(5):
            for y in range(4):
                tile = ltiles[x][y]
                if tile.row() == self.x:                                                                                    # same row
                    if tile.column() == self.y + 1 and self.y + 1 <= 3 and tile.value() == self.val and self.val > 0:       # tile on the left
                        self.val *= 2
                        self.dir = [0, 1]
                        self.alive = False
                        return False
                    if tile.column() == self.y + 1 and self.y + 1 <= 3 and tile.value() == 0:
                        self.y += 1
                        return True
        return False

    def moveDown(self, ltiles):
        if self.alive is False:
            return False

        for x in range(5):
            for y in range(4):
                tile = ltiles[x][y]
                if tile.column() == self.y:
                    if tile.row() == self.x + 1 and self.x + 1 <= 4 and tile.value() == self.val and self.val > 0:
                        self.val *= 2
                        self.dir = [1, 0]
                        self.alive = False
                        return False
                    if tile.row() == self.x + 1 and self.x + 1 <= 4 and tile.value() == 0:
                        self.x += 1
                        return True
        self.alive = False
        return False

    def moveallWayDown(self, ltiles):
        while True:
            if self.moveDown(ltiles) is False:
                return

class Image:
    def __init__(self, url, size):
        self.image = simplegui.load_image(url)
        self.sx = size[0]
        self.sy = size[1]

    def drawT(self, canvas, pos, tileNumber):
        model = -1
        while tileNumber > 1:
            model += 1
            tileNumber /= 2
        canvas.draw_image(self.image,   [model * 100 + 100 // 2, 100 // 2],             [90, 90],
                                        [pos[0] + 90 // 2, pos[1] + 90 // 2],           [90, 90])

    def drawN(self, canvas, pos):
        canvas.draw_image(self.image,   [self.sx // 2, self.sy // 2],                   [self.sx, self.sy],
                                        [self.sx // 2 + pos[0], self.sy // 2 + pos[1]], [self.sx, self.sy])

class Game:
    def __init__(self):
        self.load_resources()

        self.TICK = 0
        self.score = 0
        self.best = 0
        self.gameState = False
        self.gameDone = 0

        self.lTiles = []
        for x in range(5):
            self.lTiles.append([])
            for y in range(4):
                newTile = Tile(x, y, 0)
                self.lTiles[x].append(newTile)

        rand = random.randrange(1, 101)
        if 1 <= rand <= 60:
            rand = 2
        elif 61 <= rand <= 90:
            rand = 4
        elif 91 <= rand <= 100:
            rand = 8
        self.nextTile = rand
        self.cTile = Tile(0, random.randrange(0, 4), 2)

        self.frame = simplegui.create_frame("Tetris96", 490, 590 + 100)

        self.frame.set_keydown_handler(self.keydown)
        self.frame.set_draw_handler(self.draw_handler)

        self.timer = simplegui.create_timer(INTERVAL, self.moving_stuff)
        self.timer.start()

        self.button = self.frame.add_button("Restart", self.restart_button)

        self.label0 = self.frame.add_label(" ")
        self.label1 = self.frame.add_label("A few tips")
        self.label2 = self.frame.add_label("Move tiles left and right")
        self.label3 = self.frame.add_label("with [left][right] arrows")
        self.label4 = self.frame.add_label("Speed fall [down] arrow")
        self.label5 = self.frame.add_label("Space pause the game")

        self.sGameStart.play()
        self.frame.start()

    def restart_button(self):
        self.TICK = 0
        self.score = 0
        self.gameState = False
        self.gameDone = 0

        self.lTiles = []
        for x in range(5):
            self.lTiles.append([])
            for y in range(4):
                newTile = Tile(x, y, 0)
                self.lTiles[x].append(newTile)

        rand = random.randrange(1, 101)
        if 1 <= rand <= 60:
            rand = 2
        elif 61 <= rand <= 90:
            rand = 4
        elif 91 <= rand <= 100:
            rand = 8
        self.nextTile = rand
        self.cTile = Tile(0, random.randrange(0, 4), 2)

        self.sGameStart.play()

    def matrix(self):
        for x in range(5):
            for y in range(4):
                print str(self.lTiles[x][y])
        print

    def load_resources(self):
        self.iTile = Image("https://dl.dropboxusercontent.com/u/3381080/tetris/tiles.png", [1300, 100])
        self.iGrid = Image("https://dl.dropboxusercontent.com/u/3381080/tetris/grid.png", [490, 590])
        self.iScore = Image("https://dl.dropboxusercontent.com/u/3381080/tetris/score.png", [490, 100])
        self.sGameOver = simplegui.load_sound('https://dl.dropboxusercontent.com/u/3381080/tetris/GameOver.ogg')
        self.sGameStart = simplegui.load_sound('https://dl.dropboxusercontent.com/u/3381080/tetris/GameStart.ogg')
        self.sPieceHardDrop = simplegui.load_sound('https://dl.dropboxusercontent.com/u/3381080/tetris/PieceHardDrop.ogg')
        self.sPieceLock = simplegui.load_sound('https://dl.dropboxusercontent.com/u/3381080/tetris/PieceLockdown.ogg')
        self.sSplash = simplegui.load_sound('https://dl.dropboxusercontent.com/u/3381080/tetris/Splash.ogg')

    def moving_stuff(self):
        if self.gameState is False:             # pause
            return

        if self.gameDone == 1:
            return

        self.TICK += 1

        if self.TICK % 25 == 0:
            self.cTile.moveDown(self.lTiles)

        if self.cTile.isAlive() is False:
            loc = self.cTile.direction()

            if loc[0] != loc[1]:
                self.score += 50
                self.sSplash.play()

            self.lTiles[self.cTile.row() + loc[0]][self.cTile.column() + loc[1]] = Tile(self.cTile.row() + loc[0], self.cTile.column() + loc[1], self.cTile.value())
            rand = random.randrange(1, 101)
            if 0 <= rand <= 60:
                rand = 2
            elif 61 <= rand <= 90:
                rand = 4
            elif 91 <= rand <= 100:
                rand = 8
            position = random.randrange(0, 4)

            if self.lTiles[0][position].value() > 0:
                self.gameState = not self.gameState
                self.gameDone = 1
                self.sGameOver.play()
                if self.best < self.score:
                    self.best = self.score
                return

            self.cTile = Tile(0, position, self.nextTile)
            self.sPieceLock.play()
            self.score += 1
            self.nextTile = rand

        for i in range(4):
            for x in range(1, 4):
                for y in range(4):
                    if self.lTiles[x+1][y].value() == self.lTiles[x][y].value() and self.lTiles[x][y].value() > 0:
                        self.lTiles[x+1][y].double()
                        self.lTiles[x][y].reset()
                        self.score += 50
                        self.sSplash.play()
                        #self.matrix()
                    if self.lTiles[x+1][y].value() == 0 and self.lTiles[x][y].value() > 0:
                        self.lTiles[x+1][y].update(self.lTiles[x][y].value())
                        self.lTiles[x][y].reset()
                        #self.matrix()

    def keydown(self, key):
        if self.gameDone == 1:
            return

        if self.gameState is True:
            if key == simplegui.KEY_MAP["left"]:
                self.cTile.moveLeft(self.lTiles)
            if key == simplegui.KEY_MAP["right"]:
                self.cTile.moveRight(self.lTiles)
            if key == simplegui.KEY_MAP["down"]:
                self.cTile.moveallWayDown(self.lTiles)
                self.sPieceHardDrop.play()
                self.score += 10

        if key == simplegui.KEY_MAP["space"]:           # un-pause
            self.gameState = not self.gameState

    def draw_handler(self, canvas):
        self.iGrid.drawN(canvas, [0, 100])
        self.iScore.drawN(canvas, [0, 0])

        canvas.draw_text(str(self.score), [160, 75], 40, "White")
        canvas.draw_text(str(self.best), [280, 75], 35, "White")
        canvas.draw_text(str(self.nextTile), [420, 75], 40, "White")

        if self.gameState is True:
            canvas.draw_polygon([[0, 50], [0, 100], [150, 100], [150, 50]], 1, '#BBAD9F', '#BBAD9F')
        else:
            canvas.draw_polygon([[0, 0], [0, 50], [150, 50], [150, 0]], 1, '#BBAD9F', '#BBAD9F')

        for x in range(5):
            for y in range(4):
                self.iTile.drawT(canvas, [y * 100 + 50, x * 100 + 150], self.lTiles[x][y].value())

        self.iTile.drawT(canvas, [self.cTile.column() * 100 + 50, self.cTile.row() * 100 + 150], self.cTile.value())

newGame = Game()