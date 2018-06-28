try:
    import simplegui
except:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

import random

SCREEN_W = 800
SCREEN_H = 600
CHARS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

class Char:
    def __init__(self, pozI, ageI, colorI):
        self.char = random.choice(CHARS)
        self.poz = pozI
        self.age = ageI
        self.color = colorI

    def draw(self, canvas):
        canvas.draw_text(self.char, self.poz, 20, self.color)

    def update(self):
        self.char = random.choice(CHARS)
        self.age -= 1
        self.color -= 1

class Engine:
    def __init__(self):
        self.frame = simplegui.create_frame("Codeskulptor Matrix : @bysorynyos", SCREEN_W, SCREEN_H, 0)

        self.frame.set_draw_handler(self.drawHandler)

        #timer = simplegui.create_timer(10, self.timerHandler)
        #timer.start()

        self.frame.start()

    def drawHandler(self, canvas):
        pass


# Start the Engine
newInstance = Engine()