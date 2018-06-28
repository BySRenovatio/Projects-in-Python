# -*- coding: utf-8 -*-

import pygame
import random
import time
import sys

SCREEN_SIZE = [1920, 1080]
TEXT_SIZE = 15

CHARS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"


class delayTime:
    def __init__(self, frame_rate):
        self.frame_rate = 1.0 / (frame_rate / 100.0)
        self.time = 0
        self.prev_time = 0
        self.time_passed = 0

    def update(self):
        self.time = time.time()
        self.time_passed = self.time - self.prev_time
        if self.time_passed < self.frame_rate:
            time.sleep((self.frame_rate - self.time_passed) / 100.0)
        self.prev_time = self.time


class OneString:
    def __init__(self, pos, frame, code):
        self.pos = [int(pos[0]), int(pos[1])]
        self.frame = int(frame)
        self.max_life = 75
        self.life = int(self.max_life)
        self.fade_time = 25
        self.code = code
        self.dead = False

    def modernize(self, fail1, fail2):
        self.frame += random.randint(1, 3) / 10.0
        if self.frame >= len(self.code):
            self.frame = 0

        self.life -= 1
        if self.life <= 0:
            self.dead = True

    def render(self, screen, text):
        if self.life > self.fade_time:
            color = [200 * (float(self.life - self.fade_time) / (self.max_life - self.fade_time)), 255, 200*(float(self.life - self.fade_time)/(self.max_life - self.fade_time))]
        else:
            color = [0, 255*(float(self.life)/self.fade_time), 0]

        text_surface = text.render(self.code[int(self.frame)], False, color)
        rect = text_surface.get_rect(center=self.pos)

        screen.blit(text_surface, rect)
        return [rect]


class GroupString:
    def __init__(self, pos, speed):
        self.code = list(CHARS)
        random.shuffle(self.code, random.random)
        self.speed = int(speed)
        self.pos = [int(pos[0]), int(pos[1])]
        self.frame = 0
        self.update = 0
        self.particals = [OneString(self.pos, self.frame, self.code)]
        self.dead = False

    def modernize(self, text, size):
        self.update += 1
        if self.update == self.speed:
            self.update = 0

            if self.pos[1] < size[1]:
                self.pos[1] += text.get_height()
                self.particals.append(OneString(self.pos, int(self.frame), self.code))

            if len(self.particals) == 0:
                self.dead = True

        for partical in self.particals:
            partical.modernize(text, size)
            if partical.dead:
                self.particals.remove(partical)

        self.frame += 1
        if self.frame >= len(self.code):
            self.frame = 0

    def render(self, screen, text):
        rects = []
        for partical in self.particals:
            rects.append(partical.render(screen, text)[0])
        return rects


class Engine:
    def __init__(self):
        pygame.init()
        pygame.mouse.set_visible(False)

        self.screen = pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN)
        self.delay = delayTime(75)

        self.text = pygame.font.SysFont("Terminal", TEXT_SIZE)

        self.groups = []
        self.add_line = 1

        self.pos = random.randint(1, SCREEN_SIZE[0] / TEXT_SIZE + 1) * TEXT_SIZE - TEXT_SIZE / 2

        while True:
            self.drawHandler()

    def drawHandler(self):

        self.add_line -= 1

        if self.add_line == 0:
            fast = random.randint(0, 20)
            if fast == 0:
                speed = 3
            else:
                speed = random.randint(1, 2)

            self.add_line = 2
            self.pos = random.randint(1, SCREEN_SIZE[0] / TEXT_SIZE) * TEXT_SIZE - TEXT_SIZE / 2
            self.groups.append(GroupString([self.pos, -self.text.get_height()], speed))

        if random.randint(0, 50) == 50:
            code = list(CHARS)
            random.shuffle(code, random.random)
            self.pos = [random.randint(1, SCREEN_SIZE[0] / TEXT_SIZE + 1) * TEXT_SIZE - TEXT_SIZE / 2, random.randint(1, SCREEN_SIZE[1] / self.text.get_height() + 1) * self.text.get_height()]
            self.groups.append(OneString(self.pos, random.randint(0, len(code) - 1), code))

        for group in self.groups:
            group.modernize(self.text, SCREEN_SIZE)
            if group.dead:
                self.groups.remove(group)

        rects = []
        for group in self.groups:
            for rect in group.render(self.screen, self.text):
                rects.append(rect)

        self.delay.update()

        pygame.display.flip()

        for rect in rects:
            self.screen.fill([0, 0, 0], rect)

        self.quitHandler()

    def quitHandler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()


# Start the Engine
newInstance = Engine()