import simplegui
import random

VER = "1.0.1"
DATE = "04-05-2014"

class Player:
    def __init__(self, pos, image, narrow, imagArrow):
        self.x = pos[0]
        self.y = pos[1]
        self.direup = False
        self.dirdown = False
        self.image = image
        self.arrowID = 0
        self.nArrow = narrow
        self.lArrows = []
        self.iArrow = imagArrow

    def draw(self, canvas):
        canvas.draw_image(self.image, [750 // 2, 977 // 2], [750, 977], [self.x + 750 // 10, self.y + 977 // 10], [750 // 5, 977 // 5])

    def move(self):
        if self.direup is True and self.dirdown is False:
            if self.y - 25 >= -50:
                self.y -= 25
        elif self.dirdown is True and self.direup is False:
            if self.y + 25 <= 650:
                self.y += 25

    def movedir(self, direct):
        if direct == 'up':
            self.direup = True
        elif direct == 'down':
            self.dirdown = True
        elif direct == 'stopup':
            self.direup = False
        elif direct == 'stopdown':
            self.dirdown = False

    def lunchArrow(self):
        if self.nArrow > 0:
            self.nArrow -= 1
            self.arrowID += 1
            newArrow = Arrow(self.arrowID, [80, self.y + 70], self.iArrow)
            self.lArrows.append(newArrow)

    def arrowsNr(self):
        return self.nArrow

    def addArrows(self, value):
        self.nArrow += value

    def arrowList(self):
        return self.lArrows


class Arrow:
    def __init__(self, arrowid, pos, imArrow):
        self.x = pos[0]
        self.y = pos[1]
        self.id = arrowid
        self.rect = Rect([self.x - 811 // 16, self.y - 206 // 16], [self.x + 811 // 16, self.y + 206 // 16])
        self.iArrow = imArrow
        self.mrkDelete = False

    def draw(self, canvas):
        canvas.draw_image(self.iArrow, [811 // 2, 206 // 2], [811, 206], [self.x + 811 // 16, self.y + 206 // 16], [811 // 8, 206 // 8])

    def move(self):
        if self.x + 25 <= 1300:
            self.x += 25
            self.rect = Rect([self.x - 811 // 16, self.y - 206 // 16], [self.x + 811 // 16, self.y + 206 // 16])
        else:                       # out of bounds
            self.mrkDelete = True

    def isMarked(self):
        return self.mrkDelete

    def arrowID(self):
        return self.id

    def hittedBallon(self, ballon):
        return self.rect.overlap(self.rect, ballon.get_rect())


class Rect:
    def __init__(self, p1, p2):
        self.left = min(p1[0], p2[0])
        self.right = max(p1[0], p2[0])
        self.bottom = min(p1[1], p2[1])
        self.top = max(p1[1], p2[1])

    def __str__(self):
        string = ""
        string += "Left: " + str(self.left)
        string += " Right: " + str(self.right)
        string += " Bottom: " + str(self.bottom)
        string += " Top: " + str(self.top)
        return string

    def overlap(self, r1, r2):
        h_overlaps = (r1.left <= r2.right) and (r1.right >= r2.left)
        v_overlaps = (r1.bottom <= r2.top) and (r1.top >= r2.bottom)
        return h_overlaps and v_overlaps


class Baloon:
    def __init__(self, pos, speed, imageA, imageD, btype):
        self.x = pos[0]
        self.y = pos[1]
        self.rect = Rect([self.x - 323 // 12, self.y - 410 // 12], [self.x + 323 // 12, self.y + 410 // 12])
        self.speed = speed
        self.model = btype
        self.life = (5 - speed) // 2 + 1
        self.state = True               # alive going up
        self.markDelete = False
        self.grantedArrows = False
        self.aliveI = imageA
        self.deadI = imageD
        self.arrowIDs = []

    def draw(self, canvas):
        if self.state is True:          # draw the full ballon
            canvas.draw_image(self.aliveI, [self.model * 323 + 323 // 2, 410 // 2], [323, 410], [self.x + 323 // 12, self.y + 410 // 12], [323 // 6, 410 // 6])
        else:                           # draw the falling one
            canvas.draw_image(self.deadI, [self.model * 323 + 323 // 2, 133 // 2], [323, 133], [self.x + 323 // 12, self.y + 133 // 12], [323 // 6, 133 // 6])

    def move(self):
        if self.state is True:          # move up
            if self.y - self.speed >= -50:
                self.y -= self.speed
                self.rect = Rect([self.x - 323 // 12, self.y - 410 // 12], [self.x + 323 // 12, self.y + 410 // 12])
            else:                       # out of the bounds
                self.markDelete = True
        elif self.state is False:       # move down
            if self.y + self.speed <= 800:
                self.y += self.speed
                self.rect = Rect([self.x - 323 // 12, self.y - 410 // 12], [self.x + 323 // 12, self.y + 410 // 12])
            else:                       # out of bounds
                self.markDelete = True

    def markHitted(self, arrID):
        if self.life == 0:
            self.state = False
        else:
            for val in self.arrowIDs:
                if val == arrID:
                    return
            self.arrowIDs.append(arrID)
            self.life -= 1

    def score(self):
        if self.grantedArrows is False:
            self.grantedArrows = True
            return ((5 - self.speed) // 2 + 1), 1
        return 0, 0

    def isMarked(self):
        return self.markDelete

    def isAlive(self):
        return self.state

    def get_rect(self):
        return self.rect


class Game:
    def __init__(self):
        self.load_resources()

        self.TICKS = 0
        self.SCORE = 0
        self.ESC = False

        self.PLAYER = Player([0, 0], self.iPlayer, 33, self.iArrow)

        self.lBALLONS = []
        newBallon = Baloon([random.randrange(200, 1250, 20), 800], random.randrange(0, 6), self.iBallonA, self.iBallonD, random.randrange(0, 6))
        self.lBALLONS.append(newBallon)

        self.frame = simplegui.create_frame("Ballons " + VER, 1280, 800, 200)
        self.frame.start()

    def add_key_handlers(self):
        self.frame.set_keydown_handler(self.keydown)
        self.frame.set_keyup_handler(self.keyup)

    def add_draw_handler(self):
        self.frame.set_draw_handler(self.draw)

    def add_timer(self):
        timer = simplegui.create_timer(40, self.moving_objects)
        timer.start()

    def add_labels(self):
        self.label1 = self.frame.add_label("Score = 0")
        self.label2 = self.frame.add_label("Arrows = 33")
        self.label20 = self.frame.add_label(" ")
        self.label4 = self.frame.add_label("=== === Tips === ===")
        self.label30 = self.frame.add_label(" ")
        self.label31 = self.frame.add_label("Press ESC for pause")
        self.label3 = self.frame.add_label(" ")
        self.label5 = self.frame.add_label("Move archer with")
        self.label6 = self.frame.add_label("keyUp / keyDown")
        self.label21 = self.frame.add_label(" ")
        self.label7 = self.frame.add_label("Lunch an arrow with 'Space'")
        self.label22 = self.frame.add_label(" ")
        self.label8 = self.frame.add_label("Keep an eye on arrows left!")
        self.label23 = self.frame.add_label(" ")
        self.label9 = self.frame.add_label("You lose one arrow if")
        self.label10 = self.frame.add_label("a ballon escapes!")
        self.label24 = self.frame.add_label(" ")
        self.label11 = self.frame.add_label("Depending on the speed, some ballons have more than one life. Lower speed ballons have more life; higher speed ones have less.")
        self.label25 = self.frame.add_label(" ")
        self.label12 = self.frame.add_label("You get back the number of arrows used to down a ballon.")

    def moving_objects(self):
        if self.ESC is True:
            return

        if self.PLAYER.arrowsNr() > 0:
            self.TICKS += 1
            self.PLAYER.move()

            if self.TICKS % 25 == 0:
                newBallon = Baloon([random.randrange(200, 1250, 20), 800], random.randrange(0, 6), self.iBallonA, self.iBallonD, random.randrange(0, 6))
                self.lBALLONS.append(newBallon)

            for ballon in self.lBALLONS:
                if ballon.isAlive() is False:
                    bScore, bArr = ballon.score()
                    self.SCORE += bScore
                    self.PLAYER.addArrows(bArr)
                    if bArr == 1:
                        self.sExp.play()
                    self.label1.set_text("Score = " + str(self.SCORE))
                    self.label2.set_text("Arrows = " + str(self.PLAYER.arrowsNr()))
                if ballon.isMarked() is True:
                    self.lBALLONS.remove(ballon)
                    if ballon.isAlive() is True:
                        newBallon = Baloon([random.randrange(200, 1250, 20), 800], random.randrange(0, 6), self.iBallonA, self.iBallonD, random.randrange(0, 6))
                        self.lBALLONS.append(newBallon)
                        self.PLAYER.addArrows(-1)           # lose one arrow if you miss a ballon
                        self.label2.set_text("Arrows = " + str(self.PLAYER.arrowsNr()))

            for arrow in self.PLAYER.arrowList():
                for ballon in self.lBALLONS:
                    if arrow.hittedBallon(ballon) is True:
                        ballon.markHitted(arrow.arrowID())

            for ballon in self.lBALLONS:
                ballon.move()

            for arrow in self.PLAYER.arrowList():
                if arrow.isMarked() is True:
                    self.PLAYER.arrowList().remove(arrow)

            for arrow in self.PLAYER.arrowList():
                arrow.move()

            if self.PLAYER.arrowsNr() == 0:
                self.sDie.play()

    def load_resources(self):
        self.iBackground = simplegui.load_image('https://dl.dropboxusercontent.com/u/3381080/ballon/background.jpg')
        self.iPlayer = simplegui.load_image('https://dl.dropboxusercontent.com/u/3381080/ballon/archer.png')
        self.iBallonA = simplegui.load_image('https://dl.dropboxusercontent.com/u/3381080/ballon/ballons.png')
        self.iBallonD = simplegui.load_image('https://dl.dropboxusercontent.com/u/3381080/ballon/seats.png')
        self.iArrow = simplegui.load_image('https://dl.dropboxusercontent.com/u/3381080/ballon/arrow.png')
        self.iwin = simplegui.load_image("https://dl.dropboxusercontent.com/u/3381080/ballon/win.png")
        self.ihelp = simplegui.load_image("https://dl.dropboxusercontent.com/u/3381080/ballon/help.png")
        self.sMove = simplegui.load_sound('https://dl.dropboxusercontent.com/u/3381080/ballon/sound_footstep.wav')
        self.sDie = simplegui.load_sound('https://dl.dropboxusercontent.com/u/3381080/ballon/sound_die.wav')
        self.sArrow = simplegui.load_sound('https://dl.dropboxusercontent.com/u/3381080/ballon/sound_click.wav')
        self.sExp = simplegui.load_sound('https://dl.dropboxusercontent.com/u/3381080/ballon/sound_explosion.wav')

    def draw_background(self, canvas):
        canvas.draw_image(self.iBackground, [2560 // 2, 1600 // 2], [2560, 1600], [1280 // 2, 800 // 2], [2560 // 2, 1600 // 2])

    def draw_help(self, canvas):
        canvas.draw_image(self.ihelp, [1280 // 2, 800 // 2], [1280, 800], [1280 // 2, 800 // 2], [1280, 800])

    def draw(self, canvas):
        if self.ESC is False:
            self.draw_background(canvas)
            self.PLAYER.draw(canvas)

            for ballon in self.lBALLONS:
                ballon.draw(canvas)

            for arrow in self.PLAYER.arrowList():
                arrow.draw(canvas)

            if self.PLAYER.arrowsNr() <= 0:
                canvas.draw_image(self.iwin, [440 // 2, 131 // 2], [440, 131], [1280 // 2, 800 // 2], [440 * 2, 131 * 2])
        else:
            self.draw_help(canvas)

    def keydown(self, key):
        if key == 27:                               # esc
            self.ESC = not self.ESC

        if key == simplegui.KEY_MAP['up']:
            self.PLAYER.movedir('up')
            self.sMove.play()
        elif key == simplegui.KEY_MAP['down']:
            self.PLAYER.movedir('down')
            self.sMove.play()
        elif key == simplegui.KEY_MAP['space']:
            self.PLAYER.lunchArrow()
            self.label2.set_text("Arrows = " + str(self.PLAYER.arrowsNr()))
            self.sArrow.play()

    def keyup(self, key):
        if key == simplegui.KEY_MAP['up']:
            self.PLAYER.movedir('stopup')
        elif key == simplegui.KEY_MAP['down']:
            self.PLAYER.movedir('stopdown')

newGame = Game()
newGame.add_key_handlers()
newGame.add_draw_handler()
newGame.add_labels()
newGame.add_timer()