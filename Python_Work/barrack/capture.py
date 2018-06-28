import simplegui
import random

VER = "2.0.1"
DATE = "03-05-2014"
INTERVAL = 40                   # 25 FPS

# the two images for the win/lose state
ilose = simplegui.load_image("https://dl.dropboxusercontent.com/u/3381080/barrack/lost.gif")
iwin = simplegui.load_image("https://dl.dropboxusercontent.com/u/3381080/barrack/win.png")

class Player:
    def __init__(self, timer):
        # player position ... top left corner of the screen
        self.x = 100
        self.y = 100

        # life, speed and score
        self.life = 3
        self.speed = 1
        self.score = 0

        # initial period that we have available and the current time
        self.time = timer
        self.timeI = timer

        # bonus message to show
        self.bonus = "None"

        # invincible and how many ticks should be invincible
        self.invincible = False
        self.invticks = 0

    # draw 3 circles as a player
    def draw(self, canvas):
        canvas.draw_circle([self.x, self.y], 6, 2, "Blue")
        canvas.draw_circle([self.x, self.y], 4, 2, "Yellow")
        canvas.draw_circle([self.x, self.y], 2, 2, "Red")

    def move(self, poz):
        # every time a move is to happen
        self.time -= 1
        self.invticks -= 1

        # out of the bounds ? don't allow
        if 0 <= poz[0] <= 800:
            self.x = poz[0]
        if 50 <= poz[1] <= 600:
            self.y = poz[1]

        # invincible period has passed
        # make it non invincible
        if self.invticks == 0:
            self.invincible = False

    # 750 = 30s of invincibility
    def set_invincible(self):
        self.invticks = 750
        self.invincible = True

    # life as string
    def get_life(self):
        return str(self.life)

    # is or not invincible
    def get_invincible(self):
        return self.invincible

    # life as a value
    def get_lifev(self):
        return self.life

    # add a life
    def add_life(self):
        self.life += 1

    # lose a life
    def lose_life(self):
        self.life -= 1

    # get speed as number
    def get_speed(self):
        return self.speed

    # how much of the screen was covered ? as string
    def get_score(self):
        return str(self.score / (80 * 50.0))

    # add a procent to the existing one
    def add_score(self, val):
        self.score += val

    # get the score as a value
    def get_scorev(self):
        return (self.score / (80 * 50.0))

    # get the time as a string
    def get_times(self):
        return str(self.time//25)

    # current time remaining in seconds
    def get_time(self):
        return (self.time//40)

    # initial time in seconds
    def get_timeMax(self):
        return (self.timeI//40)

    # location as a [x, y] pair
    def get_location(self):
        return [self.x, self.y]

    # add a minute of time
    def add_time(self):
        self.time += 60 * 25

    # return the bonus message
    def get_bonus(self):
        return self.bonus

    # set bonus string to the current one
    def set_bonus(self, str):
        self.bonus = str

class Line:
    def __init__(self, point, direction):
        # line direction
        self.dir = direction

        # starting point location
        self.x = point[0]
        self.y = point[1]

        # the 2 points on the edges
        self.p1x = point[0]
        self.p1y = point[1]
        self.p2x = point[0]
        self.p2y = point[1]

        # if the points got in contact with other lines = False
        self.p1 = True              # if not capped
        self.p2 = True              # if not capped

    def move(self):
        global LINES
        global newLine

        # horizontal direction ?
        if self.dir is True:
            # point 1 got capped ?
            if self.p1 is True:
                # move by one pixel on the left
                self.p1x -= PLAYER.get_speed()
                # touched any of the lines
                if self.hittedLine(self.p1x, self.p1y) is True:
                    # if yes mark it as capped
                    self.p1 = False
            # point 2 got capped ?
            if self.p2 is True:
                # move by one pixel on the right
                self.p2x += PLAYER.get_speed()
                # in contact with any line ?
                if self.hittedLine(self.p2x, self.p2y) is True:
                    # mark it as capped
                    self.p2 = False
        # vertical direction ?
        if self.dir is False:
            # point 1 got capped ?
            if self.p1 is True:
                # move it up by one pixel
                self.p1y -= PLAYER.get_speed()
                # got in contact ?
                if self.hittedLine(self.p1x, self.p1y) is True:
                    # mark it as capped
                    self.p1 = False
            # point 2 got ccapped
            if self.p2 is True:
                # move by one pixel down
                self.p2y += PLAYER.get_speed()
                # got in contact with any line
                if self.hittedLine(self.p2x, self.p2y) is True:
                    # mark it as capped
                    self.p2 = False
        # both points got capped
        if self.p1 is False and self.p2 is False:
            # add the line to the bouncing lines list
            LINES.append([[self.p1x, self.p1y], [self.p2x, self.p2y]])
            # if the line horizontal
            if self.dir is True:
                # try to fill the spaces up and down
                self.makepolyup([self.p1x+1, self.p1y-1], [self.p2x-1, self.p2y-1])
                self.makepolydown([self.p1x+1, self.p1y+1], [self.p2x-1, self.p2y+1])
            else:
                # try to fill the spaces left and right
                self.makepolyleft([self.p1x-1, self.p1y+1], [self.p2x-1, self.p2y-1])
                self.makepolyright([self.p1x+1, self.p1y+1], [self.p2x+1, self.p2y-1])
            # delete the line
            newLine = None

    def makepolyleft(self, p1, p2):
        global POLYS
        global PLAYER
        global newbonus

        # x coords will decrese by one until a line is found
        # if they are in contact then we have the second point of our poly
        x = p2[0]
        while(x >= 0):
            x -= 1
            # check all the lines for a contact with the current point
            for line in LINES:
                if self.isBetween([line[0][0], line[0][1]], [line[1][0], line[1][1]], [x, p1[1]]) is True:
                    newPoly = [[x, p1[1]], p2]
                    minx = min(x, p2[0])
                    maxx = max(x, p2[0])
                    miny = min(p1[1], p2[1])
                    maxy = max(p1[1], p2[1])
                    # contact with a ball ? we wont fill the space
                    for ball in BALLS:
                        bcoord = ball.get_location()
                        if minx <= bcoord[0] <= maxx:
                            if miny <= bcoord[1] <= maxy:
                                return
                    # bonus inside ? then activate it /// we get here if no other ball is in this space
                    if newbonus is not None:
                        bonusc = newbonus.get_location()
                        if minx <= bonusc[0] <= maxx:
                            if miny <= bonusc[1] <= maxy:
                                newbonus.activate()
                                # delete the bonus
                                newbonus = None
                    # we got here then no ball was found in this space ... add the space covered to score
                    # add it to the poly list
                    PLAYER.add_score((maxx - minx) * (maxy - miny))
                    POLYS.append(newPoly)
                    return

    def makepolyright(self, p1, p2):
        global POLYS
        global PLAYER
        global newbonus

        # x coords will increse by one until a line is found
        # if they are in contact then we have the second point of our poly
        x = p2[0]
        # don't allow to get out of the bounds
        while(x <= 800):
            x += 1
            for line in LINES:
                 # check all the lines for a contact with the current point
                if self.isBetween([line[0][0], line[0][1]], [line[1][0], line[1][1]], [x, p1[1]]) is True:
                    newPoly = [[x, p1[1]], p2]
                    minx = min(x, p2[0])
                    maxx = max(x, p2[0])
                    miny = min(p1[1], p2[1])
                    maxy = max(p1[1], p2[1])
                    # check if a ball is inside the current rectangle
                    for ball in BALLS:
                        bcoord = ball.get_location()
                        if minx <= bcoord[0] <= maxx:
                            if miny <= bcoord[1] <= maxy:
                                return
                    # if a bonus is inside and no ball the activate it and delete it
                    if newbonus is not None:
                        bonusc = newbonus.get_location()
                        if minx <= bonusc[0] <= maxx:
                            if miny <= bonusc[1] <= maxy:
                                newbonus.activate()
                                newbonus = None
                    # update the score and add the rectangle to the list of rectangles
                    PLAYER.add_score((maxx - minx) * (maxy - miny))
                    POLYS.append(newPoly)
                    return

    def makepolyup(self, p1, p2):
        global POLYS
        global PLAYER
        global newbonus

        y = p2[1]
        # don't allow to get out of the bounds
        while(y >= 100):
            y -= 1
            # check if got in contact with any line
            for line in LINES:
                if self.isBetween([line[0][0], line[0][1]], [line[1][0], line[1][1]], [p2[0], y]) is True:
                    newPoly = [p1, [p2[0], y]]
                    minx = min(p1[0], p2[0])
                    maxx = max(p1[0], p2[0])
                    miny = min(p1[1], y)
                    maxy = max(p1[1], y)
                    # contact with any ball ?
                    # don't allow to fill the rectangle
                    for ball in BALLS:
                        bcoord = ball.get_location()
                        if minx <= bcoord[0] <= maxx:
                            if miny <= bcoord[1] <= maxy:
                                return
                    # we have a bonus inside the rectagle ?
                    # activate it and the delete it
                    if newbonus is not None:
                        bonusc = newbonus.get_location()
                        if minx <= bonusc[0] <= maxx:
                            if miny <= bonusc[1] <= maxy:
                                newbonus.activate()
                                newbonus = None
                    # update the new space covered to the existing score
                    PLAYER.add_score((maxx - minx) * (maxy - miny))
                    # add the rectangle to our list
                    POLYS.append(newPoly)
                    return

    def makepolydown(self, p1, p2):
        global POLYS
        global PLAYER
        global newbonus

        y = p2[1]
        # while intersection point not out of bounds
        while(y <= 600):
            y += 1
            # check if is in contact with any of the lines
            for line in LINES:
                if self.isBetween([line[0][0], line[0][1]], [line[1][0], line[1][1]], [p2[0], y]) is True:
                    newPoly = [p1, [p2[0], y]]
                    minx = min(p1[0], p2[0])
                    maxx = max(p1[0], p2[0])
                    miny = min(p1[1], y)
                    maxy = max(p1[1], y)
                    # contact with any ball ?
                    for ball in BALLS:
                        bcoord = ball.get_location()
                        if minx <= bcoord[0] <= maxx:
                            if miny <= bcoord[1] <= maxy:
                                return
                    # bonus inside the rectangle
                    if newbonus is not None:
                        bonusc = newbonus.get_location()
                        if minx <= bonusc[0] <= maxx:
                            if miny <= bonusc[1] <= maxy:
                                newbonus.activate()
                                newbonus = None
                    # all went good so we update the surface to the score
                    # and add our rectangle to the list
                    PLAYER.add_score((maxx - minx) * (maxy - miny))
                    POLYS.append(newPoly)
                    return

    def isBetween(self, a, b, c):
        # if c is in betwwen points a and b return true else: false
        crossproduct = (c[1] - a[1]) * (b[0] - a[0]) - (c[0] - a[0]) * (b[1] - a[1])
        if abs(crossproduct) != 0:
            return False

        dotproduct = (c[0] - a[0]) * (b[0] - a[0]) + (c[1] - a[1])*(b[1] - a[1])
        if dotproduct < 0:
            return False

        squaredlengthba = (b[0] - a[0])*(b[0] - a[0]) + (b[1] - a[1])*(b[1] - a[1])
        if dotproduct > squaredlengthba:
            return False

        return True

    def hittedLine(self, x, y):
        # if the point [x, y] is inside of a line return true; else false
        for line in LINES:
            if self.isBetween([line[0][0], line[0][1]], [line[1][0], line[1][1]], [x, y]) is True:
                return True
        return False

    def draw(self, canvas):
        # draw the half og the line (middle -> first edge) and (middle -> second edge)
        canvas.draw_line([self.x, self.y], [self.p1x, self.p1y], 1, "White")
        canvas.draw_line([self.x, self.y], [self.p2x, self.p2y], 1, "White")

    def direction(self):
        # return the direction of the line True - horizontal, False - vertical
        return self.dir

    def points(self):
        # return the two points of the line (edges) [], []
        return [[self.p1x, self.p1y], [self.p2x, self.p2y]]

class Ball:
    def __init__(self, x, y, xv, yv, speed, r):
        # ball location
        self.x = x
        self.y = y

        # ball velocities
        self.xvel = xv
        self.yvel = yv

        # ball radius
        self.radius = r

        # ball speed
        self.speed = speed

        # rectagle that fits the ball
        self.rect = [[self.x - self.radius, self.y - self.radius], [self.x + self.radius, self.y - self.radius],
                     [self.x - self.radius, self.y + self.radius], [self.x + self.radius, self.y + self.radius]]

    def contact(self, rect, a, b):
        # for each point in the ball rectangle check if it is in contact with a line [a, b]
        # return True is yes and False if not
        for x in range(rect[0][0], rect[1][0] + 1):
            for y in range(rect[0][1], rect[2][1] + 1):
                if self.isBetween(a, b, [x, y]) is True:
                    return True
        return False

    def draw(self, canvas):
        # draw a green ball with above properties
        canvas.draw_circle([self.x, self.y], self.radius, self.radius * 2, "Green")

    def isBetween(self, a, b, c):
        # if point c is on the line [a,b] return True else: False
        crossproduct = (c[1] - a[1]) * (b[0] - a[0]) - (c[0] - a[0]) * (b[1] - a[1])
        if abs(crossproduct) != 0:
            return False

        dotproduct = (c[0] - a[0]) * (b[0] - a[0]) + (c[1] - a[1])*(b[1] - a[1])
        if dotproduct < 0:
            return False

        squaredlengthba = (b[0] - a[0])*(b[0] - a[0]) + (b[1] - a[1])*(b[1] - a[1])
        if dotproduct > squaredlengthba:
            return False

        return True

    def move(self):
        global PLAYER

        # check all the lines if they are in contact with ball rectangle
        for line in LINES:
            if self.contact(self.rect, line[0], line[1]) is True:
                # if touched a horizontal line -> mirror the velocity
                if line[0][0] == line[1][0]:      # horizontal
                    self.xvel *= -1
                # if touched a vertical line -> mirror the velocity
                if line[0][1] == line[1][1]:      # vertical
                    self.yvel *= -1

        # if a line is growing
        global newLine
        if newLine is not None:
            # if player not invincible
            if PLAYER.get_invincible() is False:
                # get the coords edges of the line
                coords = newLine.points()
                # if the ball touched the line then lose a life and delete the line
                if self.contact(self.rect, coords[0], coords[1]) is True:
                    newLine = None
                    PLAYER.lose_life()

        # update the ball position
        self.x += self.xvel * self.speed
        self.y += self.yvel * self.speed

        # get a new rectangle for the ball
        self.rect[0] = [self.x - self.radius, self.y - self.radius]
        self.rect[1] = [self.x + self.radius, self.y - self.radius]
        self.rect[2] = [self.x - self.radius, self.y + self.radius]
        self.rect[3] = [self.x + self.radius, self.y + self.radius]

    def get_location(self):
        # return the ball location
        return [self.x, self.y]

    def increase_speed(self):
        # increase the ball speed
        self.speed += 1

    def decrease_speed(self):
        # decrease the ball spedd
        self.speed -= 1

    def reset_speed(self):
        # set the ball spedd 0
        self.speed = 0

    def get_speed(self):
        # ball speed as string to be able to print it on the screen
        return str(self.speed)

class Bonus:
    def __init__(self, typee):
        # bonus type
        self.ty = typee

        # ball radius is 3
        self.rad = 3

        # initial position / a ball position
        self.poz = BALLS[0].get_location()

    def draw(self, canvas):
        # set different colors depending on the bonus that grants
        color = "White"
        if self.ty == 0:                # life
            color = "Purple"
        elif self.ty == 1:              # -1 speed
            color = "Yellow"
        elif self.ty == 2:              # 0 speed
            color = "Teal"
        elif self.ty == 3:              # 60s time
            color = "Aqua"
        elif self.ty == 4:              # invincible line
            color = "Blue"
        canvas.draw_circle([self.poz[0], self.poz[1]], self.rad, self.rad * 2, color)

    def activate(self):
        # depending on the bonus value we update the
        # necesary values
        if self.ty == 0:
            # add a life + update the text to be drawn
            PLAYER.add_life()
            PLAYER.set_bonus("Life")
        if self.ty == 1:
            # decrease speed by one + update the text to be drawn
            for balls in BALLS:
                balls.decrease_speed()
            PLAYER.set_bonus("- Speed")
        if self.ty == 2:
            # set the speed to 0 + update the text
            for balls in BALLS:
                balls.reset_speed()
            PLAYER.set_bonus("0 Speed")
        if self.ty == 3:
            # add a minute of time
            PLAYER.add_time()
            PLAYER.set_bonus("Time")
        if self.ty == 4:
            # set invincible
            PLAYER.set_invincible()
            PLAYER.set_bonus("Invincible")

    def get_location(self):
        # return location of the bonus ball
        return self.poz

def draw_player(canvas):
    # draw the player image
    PLAYER.draw(canvas)

def draw_details(canvas):
    # draw the line that splits the game board and also the game details that might be interesting for the player
    canvas.draw_text("Life: " + PLAYER.get_life(), [10, 30], 30, "White")
    canvas.draw_text("Speed: " + BALLS[0].get_speed(), [110, 30], 30, "White")
    canvas.draw_text("Time: " + PLAYER.get_times() + "s", [240, 30], 30, "White")
    canvas.draw_text("Bonus: " + PLAYER.get_bonus(), [400, 30], 30, "White")
    canvas.draw_text("Score: " + PLAYER.get_score(), [620, 30], 30, "White")

def draw_gameboard(canvas):
    # draw the game board / 4 lines
    canvas.draw_polygon([[0, 100], [800, 100], [800, 600], [0, 600]], 1, "Red")

def draw_timerbar(canvas):
    # draw the timerbar poly
    canvas.draw_polygon([[0, 50], [800, 50], [800, 100], [0, 100]], 1, "Red")
    # get the distance that represents how much time has passed since the start of the game
    distance = PLAYER.get_time() * 800 // PLAYER.get_timeMax()
    #draw the filling
    canvas.draw_polygon([[0, 50], [distance, 50], [distance, 100], [0, 100]], 1, "Red", "Blue")

def draw_oneline(canvas, line):
    # draw one line at a time / line that bounces a ball
    canvas.draw_line([line[0][0], line[0][1]], [line[1][0], line[1][1]], 1, "Yellow")

def draw_lines(canvas):
    # draw all the lines that can bounce a ball / except the first 4 (game board, already drawn)
    for i in range(4, len(LINES)):
        draw_oneline(canvas, LINES[i])

    # if a growing line is in progress draw it
    if newLine is not None:
        newLine.draw(canvas)

def draw_balls(canvas):
    # draw all the balls
    for balls in BALLS:
        balls.draw(canvas)

def draw_polys(canvas):
    # draw all the polys
    for poly in POLYS:
        canvas.draw_polygon([[poly[0][0], poly[0][1]], [poly[1][0], poly[0][1]], [poly[1][0], poly[1][1]], [poly[0][0], poly[1][1]]], 1, 'Red', 'Red')

def draw_bonus(canvas):
    # if we have a bonus on the map, draw it
    if newbonus is not None:
        newbonus.draw(canvas)

def draw(canvas):
    # draw all the elements on the canvas
    draw_polys(canvas)
    draw_details(canvas)
    draw_gameboard(canvas)
    draw_timerbar(canvas)
    draw_player(canvas)
    draw_lines(canvas)
    draw_balls(canvas)
    draw_bonus(canvas)
    # if win state draw also the image with the win message
    if gameState == 1:          # win
        canvas.draw_image(iwin, [440 // 2, 131 // 2], [440, 131], [400, 400], [440, 131])
    # if we lost the game draw then draw the image specific for this state
    elif gameState == -1:       # lose
        canvas.draw_image(ilose, [500 // 2, 160 // 2], [500, 160], [400, 400], [500, 160])

def keydown(key):
    global DIRECTION
    global newLine

    # if a space was pressed
    if key == simplegui.KEY_MAP["space"]:
        # create a new growing line
        newLine = Line(PLAYER.get_location(), DIRECTION)
    # if a CTRL key was pressed; change the line direction
    if key == 17:
        if DIRECTION is True:
            DIRECTION = False
        else:
            DIRECTION = True

def mousedrag(pos):
    # get and update the mouse position variable
    global position
    position = pos

def moving_objects():
    global PLAYER
    global gameState
    global TICK
    global newbonus

    TICK += 1

    # game in progress ? state = 0
    if gameState == 0:
        # move the player to the position provided from the mouse drag handler
        PLAYER.move(position)

        # if a line is in progress / growing
        if newLine is not None:
            newLine.move()

        # 60s passed ? increase the balls speed
        for balls in BALLS:
            if TICK % 1500 == 0:
                balls.increase_speed()
            balls.move()

        # 60s passed ? make a bonus object
        if TICK % 1500 == 0:
            newbonus = Bonus(random.randrange(5))

        # life = 0 ... mark the game as lost
        if PLAYER.get_lifev() == 0:
            gameState = -1

        # time passed ? ... mark the game state as lost
        if PLAYER.get_time() == -1:
            gameState = -1

        # Covered more than 80% of the screen ? mark the game as won
        if PLAYER.get_scorev() > 80:
            gameState = 1

def init():
    # game is in progress
    global gameState
    gameState = 0

    # starting tick from 0
    global TICK
    TICK = 0

    # player starting position
    global position
    position = [100, 100]

    # direction horizontally
    global DIRECTION
    DIRECTION = True

    # list for all the filled spaces
    global POLYS
    POLYS = []

    # the bouncing lines (board)
    global LINES
    LINES = []
    LINES.append([[0, 100], [800, 100]])
    LINES.append([[800, 100], [800, 600]])
    LINES.append([[800, 600], [0, 600]])
    LINES.append([[0, 600], [0, 100]])

    # add a first ball
    global BALLS
    BALLS = []
    newBall = Ball(300, 300, 1, 1, 1, 4)
    BALLS.append(newBall)

    # no line to draw
    global newLine
    newLine = None

    # no bonus to draw
    global newbonus
    newbonus = None

    # make a player
    global PLAYER
    PLAYER = Player(4500)

def brestart():
    # restart the game
    init()

def bball():
    global BALLS
    # add a new ball starting from the first ball position but with random velocities
    coords = BALLS[0].get_location()
    newBall = Ball(coords[0], coords[1], random.randrange(-1, 2, 1), random.randrange(-1, 2, 1), 1, 4)
    BALLS.append(newBall)

def bbonus():
    # add a new bonus on the screen
    global newbonus
    newbonus = Bonus(random.randrange(5))

# frame creation
frame = simplegui.create_frame("Capture " + VER, 800, 600, 200)

# event handlers for mouse and keyboard
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_mousedrag_handler(mousedrag)

# add balls button
button0 = frame.add_button('Add bonus', bbonus, 150)

# add a space label - for a new line
label1 = frame.add_label(' ')

# add balls button
button1 = frame.add_button('Add ball', bball, 150)

# add a space label - for a new line
label2 = frame.add_label(' ')

# restart button
button2 = frame.add_button('Restart', brestart, 150)

# add a space label - for a new line
label3 = frame.add_label(' ')

# Few tips
label4 = frame.add_label('=== Help ===')
label5 = frame.add_label('Press SPACE for a line')
label6 = frame.add_label('Press CTRL to change')
label7 = frame.add_label('the direction of the line')

# start a timer to take care of the moving objects
aTimer = simplegui.create_timer(INTERVAL, moving_objects)
aTimer.start()

# initialize the objects and start the frame
init()
frame.start()