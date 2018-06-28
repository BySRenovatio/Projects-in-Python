import random

INTERVAL = 20           # 50 fps

try:
    import simplegui
except:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

class Tile:
    def __init__(self, xCoord, yCoord, xVel, iTile, model):
        self.x = xCoord                                 # top left coords
        self.y = yCoord
        self.xv = xVel
        self.model = model
        self.tdel = False
        self.newWave = False
        self.image = iTile

    def move(self):
        if self.x == 149:
            self.newWave = True

        if self.x <= 148:
            self.newWave = False

        if self.x + 135 <= 0:
            self.tdel = True
        else:
            self.x += self.xv

    def tDelete(self):
        return self.tdel

    def position(self):
        return [self.x, self.y]

    def nWave(self):
        return self.newWave

    def draw(self, canvas):
        canvas.draw_image(self.image,   [self.model * 100 + 100 // 2, 100 // 2],    [90, 90],
                                        [self.x + 95, self.y + 95],                 [90, 90])

class Player():
    def __init__(self, xCoord, yCoord, yVel, iTile, model):
        self.x = xCoord                                 # top left coords
        self.y = yCoord
        self.yv = yVel
        self.model = model
        self.image = iTile
        self.done = False

    def move(self, flap):
        if self.y > 500:
            self.yv = -7.50

        if self.y > 445:
            self.model = 13

        if self.y < -45:
            self.model = 13

        if flap:
            self.yv = -11.25

        self.yv += 0.75
        self.y += self.yv

    def change_model(self):
        if self.model == 13:
            self.model = -1
        self.model += 1
        if self.model == 12:                     # put 12 here
            self.done = True

    def reset_model(self):
        self.model = 13

    def position(self):
        return [self.x, self.y]

    def isDone(self):
        return self.done

    def get_score(self):
        if self.model == 13:
            return "1"
        return 2 ** (self.model + 1)

    def draw(self, canvas):
        canvas.draw_image(self.image,   [self.model * 100 + 100 // 2, 100 // 2],    [90, 90],
                                        [self.x + 95, self.y + 95],                 [90, 90])

class Game:
    def __init__(self):
        self.load_resources()

        self.bestScore = 1
        self.newWave = False
        self.lastWave = 1
        self.TICKS = 0
        self.tSpeed = -8

        self.lTiles = []
        self.lTiles.append(Tile(445, 0, self.tSpeed, self.ImagTile, 14))
        self.lTiles.append(Tile(445, 100, self.tSpeed, self.ImagTile, 14))
        self.lTiles.append(Tile(445, 400, self.tSpeed, self.ImagTile, 14))

        self.PLAYER = Player(0, 500, 0, self.ImagTile, 13)

        self.frame = simplegui.create_frame("Flappy Bird 4096 version", 490, 590)

        self.frame.set_keydown_handler(self.keydown)
        self.frame.set_draw_handler(self.draw_handler)
        self.frame.set_mouseclick_handler(self.mouseclick)

        self.timer = simplegui.create_timer(INTERVAL, self.moving_stuff)
        self.timer.start()

        self.label1 = self.frame.add_label("Score = 1")
        self.label2 = self.frame.add_label("Best Score = 1")
        self.timel = self.frame.add_label("Time = 0s")
        self.label3 = self.frame.add_label(" ")
        self.button = self.frame.add_button("Restart", self.restart_game)

        self.frame.start()

    def restart_game(self):
        self.bestScore = 1
        self.newWave = False
        self.lastWave = 1
        self.TICKS = 0

        self.lTiles = []
        self.lTiles.append(Tile(445, 0, self.tSpeed, self.ImagTile, 14))
        self.lTiles.append(Tile(445, 100, self.tSpeed, self.ImagTile, 14))
        self.lTiles.append(Tile(445, 400, self.tSpeed, self.ImagTile, 14))

        self.PLAYER = Player(0, 500, 0, self.ImagTile, 13)

        self.label1.set_text("Score = 1")
        self.label2.set_text("Best Score = 1")
        self.timel.set_text("Time = 0s")


    def load_resources(self):
        self.ImagTile = simplegui.load_image("https://dl.dropboxusercontent.com/u/3381080/flappy/8192.png")
        self.ImagBackground = simplegui.load_image("https://dl.dropboxusercontent.com/u/3381080/flappy/grid.png")
        self.iWin = simplegui.load_image("https://dl.dropboxusercontent.com/u/3381080/flappy/win.png")
        self.sBump = simplegui.load_sound("https://dl.dropboxusercontent.com/u/3381080/flappy/Point.mp3")
        self.sJump = simplegui.load_sound("https://dl.dropboxusercontent.com/u/3381080/flappy/Jump.mp3")
        self.sIntro = simplegui.load_sound("https://dl.dropboxusercontent.com/u/3381080/flappy/Intro.mp3")

    def tImpact(self, p1, p2):
        p1left = min(p1[0], p1[0] + 90)
        p1right = max(p1[0], p1[0] + 90)
        p1bottom = min(p1[1], p1[1] + 90)
        p1top = max(p1[1], p1[1] + 90)

        p2left = min(p2[0], p2[0] + 90)
        p2right = max(p2[0], p2[0] + 90)
        p2bottom = min(p2[1], p2[1] + 90)
        p2top = max(p2[1], p2[1] + 90)

        hoverlaps = True
        voverlaps = True
        if (p1left > p2right) or (p1right < p2left):
            hoverlaps = False
        if (p1top < p2bottom) or (p1bottom > p2top):
            voverlaps = False
        return hoverlaps and voverlaps

    def moving_stuff(self):
        if self.PLAYER.isDone():
            self.sIntro.play()
            return

        self.TICKS += 1

        self.newWave = False
        for tile in self.lTiles:
            if tile.nWave():
                self.newWave = True

        i = 0
        sw = 0
        while i < len(self.lTiles):
            if self.lTiles[i].tDelete():
                self.lTiles.pop(i)
                sw = 1
            else:
                i += 1

        if sw == 1:
            self.PLAYER.change_model()
            if self.PLAYER.get_score() > self.bestScore:
                self.bestScore = self.PLAYER.get_score()
            self.label1.set_text("Score = " + str(self.PLAYER.get_score()))
            self.label2.set_text("Best Score = " + str(self.bestScore))

        if self.newWave:
            if self.lastWave == 0:
                kind = random.randrange(0, 3) - 1
            elif self.lastWave == 1:
                kind = random.randrange(0, 3)
            elif self.lastWave == 2:
                kind = random.randrange(0, 3) + 1
            elif self.lastWave == 3:
                kind = random.randrange(0, 3) + 2

            if kind == 4:
                kind = 2
            elif kind == -1:
                kind = 1

            if kind == 0:
                self.lastWave = kind
                self.lTiles.append(Tile(445, 200, self.tSpeed, self.ImagTile, 14))
                self.lTiles.append(Tile(445, 300, self.tSpeed, self.ImagTile, 14))
                self.lTiles.append(Tile(445, 400, self.tSpeed, self.ImagTile, 14))
            elif kind == 1:
                self.lastWave = kind
                self.lTiles.append(Tile(445, 0, self.tSpeed, self.ImagTile, 14))
                self.lTiles.append(Tile(445, 300, self.tSpeed, self.ImagTile, 14))
                self.lTiles.append(Tile(445, 400, self.tSpeed, self.ImagTile, 14))
            elif kind == 2:
                self.lastWave = kind
                self.lTiles.append(Tile(445, 0, self.tSpeed, self.ImagTile, 14))
                self.lTiles.append(Tile(445, 100, self.tSpeed, self.ImagTile, 14))
                self.lTiles.append(Tile(445, 400, self.tSpeed, self.ImagTile, 14))
            elif kind == 3:
                self.lastWave = kind
                self.lTiles.append(Tile(445, 0, self.tSpeed, self.ImagTile, 14))
                self.lTiles.append(Tile(445, 100, self.tSpeed, self.ImagTile, 14))
                self.lTiles.append(Tile(445, 200, self.tSpeed, self.ImagTile, 14))

        for tile in self.lTiles:
            if self.tImpact(tile.position(), self.PLAYER.position()):
                self.PLAYER.reset_model()
                poz = self.PLAYER.position()
                if poz[1] <= 400:
                    self.sBump.play()
            tile.move()

        self.PLAYER.move(False)

        self.timel.set_text("Time = " + str(self.TICKS // 50) + "s")

    def keydown(self, key):
        if self.PLAYER.isDone():
            return

        if key == simplegui.KEY_MAP['space']:
            self.PLAYER.move(True)
            self.sJump.play()

    def mouseclick(self, pos):
        if self.PLAYER.isDone():
            return

        self.PLAYER.move(True)
        self.sJump.play()

    def draw_handler(self, canvas):
        canvas.draw_image(self.ImagBackground, [490 // 2, 590 // 2], [490, 590], [490 // 2, 590 // 2], [490, 590])

        for tile in self.lTiles:
            tile.draw(canvas)

        self.PLAYER.draw(canvas)

        if self.PLAYER.isDone():
            canvas.draw_image(self.iWin, [440 // 2, 131 // 2], [440, 131], [490 // 2, 590 // 2], [440, 131])

newGame = Game()