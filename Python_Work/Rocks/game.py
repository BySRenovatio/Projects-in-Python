# designed in PyCharm so
# "SimpleGUICS2Pygame.simpleguics2pygame" is the equivalent for simplegui
try:
    import simplegui
except:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
ROCK_MAX = 12
score = 0
lives = 3
time = 0.5
started = False


class ImageInfo:
    def __init__(self, center, size, radius=0, lifespan=None, animated=False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()

    def draw(self, canvas):
        if self.thrust:
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0], self.image_center[1]],
                              self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                              self.pos, self.image_size, self.angle)

    def update(self):
        # update angle
        self.angle += self.angle_vel

        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT

        # update velocity
        if self.thrust:
            acc = [math.cos(self.angle), math.sin(self.angle)]
            self.vel[0] += acc[0] * .1
            self.vel[1] += acc[1] * .1

        self.vel[0] *= .99
        self.vel[1] *= .99

    def set_thrust(self, on):
        self.thrust = on
        if on:
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()

    def increment_angle_vel(self):
        self.angle_vel += .05

    def decrement_angle_vel(self):
        self.angle_vel -= .05

    def shoot(self):
        global missile_group
        forward = [math.cos(self.angle), math.sin(self.angle)]
        missile_pos = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
        missile_vel = [self.vel[0] + 6 * forward[0], self.vel[1] + 6 * forward[1]]
        missile_group.add(Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound))

    def get_position(self):
        return self.pos

    def get_radius(self):
        return self.radius


# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound=None):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()

    def draw(self, canvas):
        if self.animated:
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0] * self.age, self.image_center[1]],
                              self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                              self.pos, self.image_size, self.angle)

    def update(self):
        # update angle
        self.angle += self.angle_vel

        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT

        self.age += 1
        if self.age < self.lifespan:
            return False
        return True

    def collide(self, other_object):
        if distance(self.get_position(), other_object.get_position()) <= self.get_radius() + other_object.get_radius():
            return True
        return False

    def get_position(self):
        return self.pos

    def get_radius(self):
        return self.radius


def distance(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


class Game:
    def __init__(self):
        self.load_resources()

        # initialize stuff
        self.frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

        # initialize ship and two sprites
        # global data
        global my_ship, rock_group, missile_group, explosion_group
        my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
        rock_group = set([])
        missile_group = set([])
        explosion_group = set([])

        # register handlers
        self.frame.set_keyup_handler(self.keyup)
        self.frame.set_keydown_handler(self.keydown)
        self.frame.set_mouseclick_handler(self.click)
        self.frame.set_draw_handler(self.draw)

        self.timer = simplegui.create_timer(999.9, self.rock_spawner)

        # get things rolling
        self.timer.start()
        self.frame.start()

    def load_resources(self):
        # art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
        # debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
        #                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
        global debris_info, debris_image
        debris_info = ImageInfo([320, 240], [640, 480])
        debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

        # nebula images - nebula_brown.png, nebula_blue.png
        global nebula_info, nebula_image
        nebula_info = ImageInfo([400, 300], [800, 600])
        nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.s2014.png")

        # splash image
        global splash_info, splash_image
        splash_info = ImageInfo([200, 150], [400, 300])
        splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

        # ship image
        global ship_info, ship_image
        ship_info = ImageInfo([45, 45], [90, 90], 35)
        ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

        # missile image - shot1.png, shot2.png, shot3.png
        global missile_image, missile_info
        missile_info = ImageInfo([5, 5], [10, 10], 3, 50)
        missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

        # asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
        global asteroid_image, asteroid_info
        asteroid_info = ImageInfo([45, 45], [90, 90], 40)
        asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

        # animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
        global explosion_image, explosion_info
        explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
        explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

        # sound assets purchased from sounddogs.com, please do not redistribute
        # .ogg versions of sounds are also available, just replace .mp3 by .ogg
        global soundtrack, missile_sound, ship_thrust_sound, explosion_sound
        soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
        missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
        missile_sound.set_volume(.5)
        ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
        explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

    # key handlers to control ship
    def keydown(self, key):
        global my_ship
        if key == simplegui.KEY_MAP['left']:
            my_ship.decrement_angle_vel()
        elif key == simplegui.KEY_MAP['right']:
            my_ship.increment_angle_vel()
        elif key == simplegui.KEY_MAP['up']:
            my_ship.set_thrust(True)
        elif key == simplegui.KEY_MAP['space']:
            my_ship.shoot()

    def keyup(self, key):
        global my_ship
        if key == simplegui.KEY_MAP['left']:
            my_ship.increment_angle_vel()
        elif key == simplegui.KEY_MAP['right']:
            my_ship.decrement_angle_vel()
        elif key == simplegui.KEY_MAP['up']:
            my_ship.set_thrust(False)

    # mouseclick handlers that reset UI and conditions whether splash image is drawn
    def click(self, pos):
        global started, score, lives, ROCK_MAX
        center = [WIDTH / 2, HEIGHT / 2]
        size = splash_info.get_size()
        inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
        inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
        if (not started) and inwidth and inheight:
            started = True
            ship_thrust_sound.rewind()
            explosion_sound.rewind()
            missile_sound.rewind()
            soundtrack.rewind()
            soundtrack.play()
            score = 0
            lives = 3
            ROCK_MAX = 12

    def draw(self, canvas):
        global time, started, lives, score, ROCK_MAX
        global my_ship, rock_group, missile_group, explosion_group

        # animiate background
        time += 1
        center = debris_info.get_center()
        size = debris_info.get_size()
        wtime = (time / 8) % center[0]
        canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2],
                          [WIDTH, HEIGHT])
        canvas.draw_image(debris_image, [center[0] - wtime, center[1]], [size[0] - 2 * wtime, size[1]],
                          [WIDTH / 2 + 1.25 * wtime, HEIGHT / 2], [WIDTH - 2.5 * wtime, HEIGHT])
        canvas.draw_image(debris_image, [size[0] - wtime, center[1]], [2 * wtime, size[1]],
                          [1.25 * wtime, HEIGHT / 2], [2.5 * wtime, HEIGHT])

        # draw UI
        canvas.draw_text("Lives", [30, 30], 30, "White")
        canvas.draw_text("Score", [700, 30], 30, "White")
        canvas.draw_text(str(lives), [50, 60], 30, "White")
        canvas.draw_text(str(score), [720, 60], 30, "White")

        # draw and update ship
        my_ship.draw(canvas)
        my_ship.update()

        # process sprite group
        self.process_sprite_group(rock_group, canvas)
        self.process_sprite_group(missile_group, canvas)
        self.process_sprite_group(explosion_group, canvas)

        # handle collisions
        if self.group_collide(rock_group, my_ship) > 0:
            lives -= 1
        if lives == 0:
            started = False
            soundtrack.pause()
            rock_group = set([])
        score += self.group_group_collide(rock_group, missile_group)
        if score > 120:
            ROCK_MAX = score // 10

        # draw splash screen if not started
        if not started:
            canvas.draw_image(splash_image, splash_info.get_center(),
                              splash_info.get_size(), [WIDTH / 2, HEIGHT / 2],
                              splash_info.get_size())

    # timer handler that spawns a rock
    def rock_spawner(self):
        global rock_group
        rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
        rock_vel = [random.random() * .50 - .25, random.random() * .50 - .25]
        rock_avel = random.random() * .20 - .10
        if started:
            if len(rock_group) < ROCK_MAX:
                if distance(rock_pos, my_ship.get_position()) > asteroid_info.get_radius() + my_ship.get_radius():
                    rock_group.add(Sprite(rock_pos, rock_vel, 0, rock_avel, asteroid_image, asteroid_info))

    # handles group-object collisions
    def group_collide(self, group, other_object):
        global explosion_group
        collisionNo = 0
        removeElements = set([])
        for sprite in group:
            if sprite.collide(other_object):
                explosion_group.add(Sprite(sprite.pos, [0, 0], 0, 0, explosion_image, explosion_info))
                explosion_sound.rewind()
                explosion_sound.play()
                removeElements.add(sprite)
                collisionNo += 1
        if len(removeElements) > 0:
            group.difference_update(removeElements)
        return collisionNo

    # handles group-group collisions
    def group_group_collide(self, group1, group2):
        collisionNo = 0
        removeElements = set([])
        for sprite in group1:
            if self.group_collide(group2, sprite) > 0:
                removeElements.add(sprite)
                collisionNo += 1
        if len(removeElements) > 0:
            group1.difference_update(removeElements)
        return collisionNo

    # update and draw sprites
    def process_sprite_group(self, group, canvas):
        removeElements = set([])
        for sprite in group:
            sprite.update()
            sprite.draw(canvas)
            if sprite.update():
                removeElements.add(sprite)
        if len(removeElements) > 0:
            group.difference_update(removeElements)


# Start the game
newGame = Game()