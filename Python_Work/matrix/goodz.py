# -*- coding: utf-8 -*-

import pygame
from pygame.locals import*
import time
import random
import sys
pygame.init()



class CodePartical(object):
    def __init__(self, pos, frame, code):
        self.pos = [int(pos[0]),int(pos[1])]
        self.frame = int(frame)
        self.max_life = 30
        self.life = int(self.max_life)
        self.fade_time = 5
        self.code =  code
        self.dead = False

        
    def modernize(self, text, size):
        self.frame+=random.randint(1,3)/10.0
        if self.frame>=len(self.code):
            self.frame = 0

        self.life-=1
        if self.life<=0:
            self.dead = True
            
    def render(self, screen, text):
        if self.life>self.fade_time:
            color = [ 200*(float(self.life-self.fade_time)/(self.max_life-self.fade_time)) , 255 , 200*(float(self.life-self.fade_time)/(self.max_life-self.fade_time)) ]
        else:
            color = [ 0 , 255*(float(self.life)/self.fade_time) , 0 ]
            
        text_surface =  text.render(self.code[int(self.frame)], False, color)
        rect = text_surface.get_rect(center = self.pos)

        screen.blit(text_surface, rect)

        return [rect]



class Group(object):
    
    def __init__(self, pos, speed):
        self.code = list(" #$%&()*+/0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^{}¢£¥§«­±»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿıŁłŒœŠšŸŽž†‡‰")
        random.shuffle(self.code, random.random)
        self.speed=int(speed)
        self.pos =[  int(pos[0]),int(pos[1]) ]
        self.frame = 0
        self.update = 0
        self.particals = [CodePartical(self.pos, self.frame, self.code)]
        self.dead=False
        
    def modernize(self, text, size):
            
        self.update+=1
        if self.update==self.speed:
            self.update=0
            
            if self.pos[1]<size[1]:
                self.pos[1]+=text.get_height()
                self.particals.append(CodePartical(self.pos, int(self.frame), self.code))
                

            if len(self.particals)==0:
                self.dead = True

            

        for partical in self.particals:
            partical.modernize(text, size)
            if partical.dead:
                self.particals.remove(partical)

        self.frame+=1
        if self.frame>=len(self.code):
            self.frame=0

        

    def render(self, screen, text):

        rects = []
        
        for partical in self.particals:
            rects.append(  partical.render(screen, text)[0]  )

        return rects


class DelaySwitch(object):
    
    def __init__(self, frame_rate):
        # FRAME RATE IS IN FRAMES/SECOND
        self.frame_rate = 1.0/(frame_rate/100.0) # makes frame rate into milliseconds
        self.time = 0
        self.prev_time = 0
        self.time_passed = 0
    def update(self):
        self.time=time.time()
        self.time_passed = self.time-self.prev_time
        if self.time_passed>self.frame_rate:
            pass
        elif self.time_passed<self.frame_rate:
            time.sleep((self.frame_rate-self.time_passed)/100.0)
        self.prev_time = self.time



        

def anti_crash():
    # === ANTI-CRASH ===
    for event in pygame.event.get():
        if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            pygame.quit()
            sys.exit()





#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#



def main():
    size = [800,600]
    screen = pygame.display.set_mode(size)

    delay = DelaySwitch(25)

    text_width=20
    try:
        text = pygame.font.SysFont("Ocra", text_width)
    except:
        raise "You need to have Ocra font on your computer to run this program."

    groups = []

    add_line=1
    pos = random.randint(1,size[0]/text_width+1)*text_width-text_width/2

    pygame.mouse.set_visible(False)





    while True:
        
        add_line-=1
        if add_line==0:
            fast = random.randint(0,20)
            if fast==0:
                speed = 3
            else:
                speed = random.randint(1,2)

            
            add_line=2
            pos = random.randint(1,size[0]/text_width)*text_width-text_width/2
            groups.append(   Group([pos, -text.get_height()], speed)   )

        if random.randint(0,50)==50:
            code = list(" #$%&()*+/0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^{}¢£¥§«­±»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿıŁłŒœŠšŸŽž†‡‰")
            random.shuffle(code, random.random)
            pos = [  random.randint(1,size[0]/text_width+1)*text_width-text_width/2   ,   random.randint(1,size[1]/text.get_height()+1)*text.get_height()   ]
            groups.append(   CodePartical(pos, random.randint(0,len(code)-1), code)  )

        


        for group in groups:
            group.modernize(text, size)
            if group.dead:
                groups.remove(group)

        rects = []
        for group in groups:
            for rect in group.render(screen, text):
                rects.append(rect)


        delay.update()

        pygame.display.flip()

        for rect in rects:
            screen.fill([0,0,0], rect)

        anti_crash()

    

############################
############################

if __name__ == "__main__":
    main()
            
    
            
        
