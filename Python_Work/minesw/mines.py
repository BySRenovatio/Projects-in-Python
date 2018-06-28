import simplegui
import random

VER = "1.0.1"
DATE = "02-05-2014"

# needed to count the seconds that passed
TIMER = 200                         # 5 FPS

# implicit values for the game board size and number of mines
TILES = [25, 25]
MINES = 25

# resources for the game
igamedata = simplegui.load_image("https://dl.dropboxusercontent.com/u/3381080/minesw/gamedata.png")
iwin = simplegui.load_image("https://dl.dropboxusercontent.com/u/3381080/minesw/congrats.png")
ilose = simplegui.load_image("https://dl.dropboxusercontent.com/u/3381080/minesw/lost.png")

def draw(canvas):
    global drawing                          # used to count the number of frames that passed since the big field was flipped
    global toDraw                           # which tiles to draw (in the big field)
    drawing -= 1                            # decrease the frame number

    for i in range(TILES[0]):               # if the tile in the map == 1 (it is flipped so show it)
        for j in range(TILES[0]):
            if stateMap[i][j] == 1:
                posi = 30 * i               # get the position on the screen to draw it
                posj = 30 * j
                val = mapm[i][j]            # get the value of the tile 0 (no value); from 1-8 print the number
                canvas.draw_image(igamedata, [15 + val * 30, 30 / 2], [30, 30], [posi + 15, posj + 15], [30, 30])
                # 15 + val * 30 - > starting pixel of the image to show in the resource, [30, 30] the tile size in pixels

    for i in range(TILES[0]):
        for j in range(TILES[0]):
            if stateMap[i][j] == -1:        # same thing but we draw on top of the map the cross (Space + click)
                posi = 30 * i
                posj = 30 * j
                canvas.draw_image(igamedata, [15 + 330, 30 / 2], [30, 30], [posi + 15, posj + 15], [30, 30])

    for i in range(TILES[0]):
        for j in range(TILES[0]):
            if stateMap[i][j] == 0:         # means the tile is hidden so we hide the number
                posi = 30 * i
                posj = 30 * j
                canvas.draw_image(igamedata, [15 + 300, 30 / 2], [30, 30], [posi + 15, posj + 15], [30, 30])

    if 10 < drawing <= 15:                  # for a period of 5 frames
        for i in range(TILES[0]):
            for j in range(TILES[0]):
                if toDraw[i][j] == 1:       # if the tile was recently flipped
                    posi = 30 * i           # get the position
                    posj = 30 * j
                    val = 12                # value 1 of the flip animation image
                    canvas.draw_image(igamedata, [15 + val * 30, 30 / 2], [30, 30], [posi + 15, posj + 15], [30, 30])

    if 5 < drawing <= 10:                   # next 5 frames
        for i in range(TILES[0]):
            for j in range(TILES[0]):
                if toDraw[i][j] == 1:       # if we have to draw the tile animation
                    posi = 30 * i
                    posj = 30 * j
                    val = 15                # second flip animation image
                    canvas.draw_image(igamedata, [15 + val * 30, 30 / 2], [30, 30], [posi + 15, posj + 15], [30, 30])

    if 0 < drawing <= 5:                    # last 5 frames
        for i in range(TILES[0]):
            for j in range(TILES[0]):
                if toDraw[i][j] == 1:
                    posi = 30 * i
                    posj = 30 * j
                    val = 13                # third flip animation image
                    canvas.draw_image(igamedata, [15 + val * 30, 30 / 2], [30, 30], [posi + 15, posj + 15], [30, 30])

    if drawing == 0:                        # we finished the animation
        for i in range(TILES[0]):
            for j in range(TILES[0]):
                if toDraw[i][j] == 1:       # mark the tiles as flipped so we wont flip the anymore this game
                    toDraw[i][j] = 0

    if gameState == -1:                     # we lost the game
        mult = (TILES[0] * 30) / 600.0      # ratio of the image to fit all the screen with tiles
        canvas.draw_image(ilose, [565 // 2, 279 // 2], [565, 279], [TILES[0] * 15, TILES[1] * 15], [565 * mult, 279 * mult])
        # draw the image with the 'lose' message

    if gameState == 1:                      # we won
        mult = (TILES[0] * 30) / 450.0      # image ratio based on the screen size
        canvas.draw_image(iwin, [440 // 2, 131 // 2], [440, 131], [TILES[0] * 15, TILES[1] * 15], [440 * mult, 131 * mult])
        # draw the image with the 'win' message

def add(i, j):
    global mapm

    # if tile is on the game board
    # and it's not a mine
    # increase the number in the tile by one (mine nearby)
    if i in range(TILES[0]):
        if j in range(TILES[1]):
            if mapm[i][j] is not -1:
                mapm[i][j] += 1

def mark(i, j):
    global stateMap
    global fieldsLeft
    global drawing
    global toDraw

    # mark the current tile as visible
    stateMap[i][j] = 1
    # decrease by 1 the number of fields left
    fieldsLeft -= 1
    # 16 frames to make the flipping aniimation
    drawing = 16
    # mark it as a tile who needs animation
    toDraw[i][j] = 1

    # check if the next position is out of bounds / only on corners or margins
    if i-1 >= 0:    # left
        # tile is blank and also hidden
        if mapm[i-1][j] == 0 and stateMap[i-1][j] == 0:
            # go and mark it
            mark(i-1, j)
        # is it a number ? and hidded ?
        if 0 < mapm[i-1][j] < 9 and stateMap[i-1][j] == 0:
            # make it visible
            stateMap[i-1][j] = 1
            # fields left less by one
            fieldsLeft -= 1
    # out of bounds ?
    if i+1 < TILES[0]:  # right
        # tile is blank and also hidden ?
        if mapm[i+1][j] == 0 and stateMap[i+1][j] == 0:
            # go mark it
            mark(i+1, j)
        # is it a numbered tile and hidden
        if 0 < mapm[i+1][j] < 9 and stateMap[i+1][j] == 0:
            # make it visible
            stateMap[i+1][j] = 1
            # deacrease by 1 the fields left
            fieldsLeft -= 1
    # out of bounds ?
    if j-1 >= 0:    # up
        # blank tile and hidden
        if mapm[i][j-1] == 0 and stateMap[i][j-1] == 0:
            # mark it
            mark(i, j-1)
        # numbered tile and hidden ?
        if 0 < mapm[i][j-1] < 9 and stateMap[i][j-1] == 0:
            # mark it as visible
            stateMap[i][j-1] = 1
            fieldsLeft -= 1
    # out of bounds ?
    if j+1 < TILES[1]:  # down
        # is it blank ? then go mark it for god sake ...
        if mapm[i][j+1] == 0 and stateMap[i][j+1] == 0:
            mark(i, j+1)
        # numbered tile and hidden
        if 0 < mapm[i][j+1] < 9 and stateMap[i][j+1] == 0:
            # make it visible
            stateMap[i][j+1] = 1
            fieldsLeft -= 1

def mouse_handler(position):
    global stateMap
    global mapm
    global gameState
    global fieldsLeft
    global minesLeft

    # we lost or won the game ?
    # if yes then no need to accept clicks
    if gameState is not 0:
        return

    # get the screen tile silection based on mouse location
    # 30 is tile size
    i = position[0] // 30
    j = position[1] // 30

    # out of the bounds ... click outside the board
    if i > TILES[0] or j > TILES[1]:
        return

    # is space pressed ?
    if SPACE is True:
        # if the tile is hidden, mark it as crossed
        # so we cant click it again, number of mines decreased
        if stateMap[i][j] == 0:
            stateMap[i][j] = -1
            minesLeft -= 1
            return
        # if the tile is already crossed
        # deselect it and update the number of mines
        if stateMap[i][j] == -1:
            stateMap[i][j] = 0
            minesLeft += 1
            return

    # numbered tile and hidded ?
    if 0 < mapm[i][j] < 9 and stateMap[i][j] == 0:
        # make it visible
        # fileds left decreased
        stateMap[i][j] = 1
        fieldsLeft -= 1
    # bomb! and hidden ?
    elif mapm[i][j] == -1 and stateMap[i][j] == 0:
        # 14 is the value of the bomb in the image vector
        mapm[i][j] = 14
        # make it visible
        stateMap[i][j] = 1

        # iterate the game board and mark the bombs (hidden or crossed) as visible
        # 9 is the value of the bomb vector in the image vector
        # -1 is the bomb value in the map vector
        for i in range(TILES[0]):
            for j in range(TILES[1]):
                if mapm[i][j] == -1 and (stateMap[i][j] == 0 or stateMap[i][j] == -1):
                    stateMap[i][j] = 1
                    mapm[i][j] = 9

        # -1 means we lost
        gameState = -1
    # blank field ? start flipping tiles
    elif mapm[i][j] == 0 and stateMap[i][j] == 0:
        mark(i, j)

def keydown(key):
    global SPACE

    # space is pressed, mark the global variable as True
    if key == simplegui.KEY_MAP['space']:
        SPACE = True

def keyup(key):
    global SPACE

    # if the key was released then make the global variable False
    if key == simplegui.KEY_MAP['space']:
        SPACE = False

def moving_objects():
    global TICK
    global gameState
    global stateMap
    global mapm
    global minesLeft

    # game still running and more than one field are still to press
    if fieldsLeft > 0 and gameState == 0:
        # increase the cycle number
        TICK += 1
        # update the secons on the board and mines left
        # 5 Ticks / second
        label2.set_text(". . . . " + str(TICK // 5) + ' s . . . .')
        label4.set_text(". . . . " + str(minesLeft) + ' . . . .')
    # no more fields left ?
    elif fieldsLeft == 0:
        # we won, mines left = 0
        gameState = 1
        minesLeft = 0
        # update the mines left
        label4.set_text(". . . . " + str(minesLeft) + ' . . . .')
        # show all the mines that are still hidden
        for i in range(TILES[0]):
            for j in range(TILES[1]):
                if mapm[i][j] == -1 and stateMap[i][j] == 0:
                    stateMap[i][j] = 1
                    mapm[i][j] = 9

def init():
    global drawing
    global toDraw
    drawing = 0

    # if number of mines is bigger than the number of tiles, set is as maximum
    global MINES
    if MINES > TILES[0] * TILES[1]:
        MINES = TILES[0] * TILES[1]

    # space not pressed
    global SPACE
    SPACE = False

    # game in progress
    global gameState
    gameState = 0

    # no ticks yet
    global TICK
    TICK = 0

    # fields left
    global fieldsLeft
    fieldsLeft = TILES[0] * TILES[1] - MINES

    # mines left
    global minesLeft
    minesLeft = MINES

    # build the statemap (contains 0 wich means all tiles are hidden)
    # build the toDraw map which contains 0, no tiles must be animated
    global stateMap
    stateMap = [[]]
    toDraw = [[]]
    for i in range(TILES[0]):
        stateMap.append([])
        toDraw.append([])
        for j in range(TILES[1]):
            stateMap[i].append(0)
            toDraw[i].append(0)

    # build the map with 0, blank tiles
    global mapm
    mapm = [[]]
    for i in range(TILES[0]):
        mapm.append([])
        for j in range(TILES[1]):
            mapm[i].append(0)

    # put #number of mines randomly in the matrix
    mines = MINES
    while (mines > 0):
        i = random.randrange(0, TILES[0])
        j = random.randrange(0, TILES[1])
        # get a random position in the matrix
        # if was not a mine there
        # set it in the matrix and update the numbers nearby
        if mapm[i][j] is not -1:
            mines -= 1
            mapm[i][j] = -1
            add(i-1, j-1)
            add(i-1, j)
            add(i-1, j+1)
            add(i, j-1)
            add(i, j+1)
            add(i+1, j-1)
            add(i+1, j)
            add(i+1, j+1)

def input1(text):
    global TILES

    # get the values (first two at least)
    # if they are > 25 or less than 0; don't allow
    # restart the game
    vals = [int(i) for i in text.split(' ')]
    if vals[0] > 25 or vals[1] > 25:
        print "Values can't be more than 30!"
        return
    if vals[0] < 1 or vals[1] < 1:
        print "Values can't be less than 1!"
        return

    TILES[0] = vals[0]
    TILES[1] = vals[1]
    init()

def input2(text):
    global MINES

    # get the mines number from input
    # if it's not a number print a message
    # else update the number and restart the game
    try:
       x = int(text)
    except ValueError:
       print "Wrong int value!"
       return
    MINES = x
    init()

def button_handler():
    # pressed the reset button
    init()

# create the frame, that supports tops 25 tiles
frame = simplegui.create_frame("Minesweeper " + VER, 25 * 30, 25 * 30, 150)

# draw handler, mouse and keyup + keydown handlers
frame.set_draw_handler(draw)
frame.set_mouseclick_handler(mouse_handler)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

# labels for the information we want to show on the left side of the game
label1 = frame.add_label('=== Time ===')
label2 = frame.add_label('    0 s')
label3 = frame.add_label('=== Mines left ===')
label4 = frame.add_label('    0')

# just a space
label5 = frame.add_label(' ')

# the two inputs fields for map and mines, update the text to demonstrate the input format
inp1 = frame.add_input('Size [x , y]', input1, 150)
inp1.set_text(str(TILES[0]) + ' ' + str(TILES[1]))
inp2 = frame.add_input('Mines', input2, 150)
inp2.set_text(str(MINES))

# restart button
button = frame.add_button('Restart', button_handler, 150)

# another space
label6 = frame.add_label('')

# Few tips
label7 = frame.add_label('=== Help ===')
label8 = frame.add_label('Press SPACE')
label9 = frame.add_label('(and hold it)')
label10 = frame.add_label('then click to')
label11 = frame.add_label('mark a mine spot.')

# a timer event to be able to show the time elapsed since the begining of the game
leTimer = simplegui.create_timer(TIMER, moving_objects)
leTimer.start()

# init the variables and start the frame
init()
frame.start()