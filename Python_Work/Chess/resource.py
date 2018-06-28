try:
    import simplegui
except:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

# Game Boards Images
NRgameBoards = 3
gameBoards = []

# Piece sets Images
NRpieceSets = 6
pieceSets = []

# Sound sets
NRsoundSets = 8
soundSets = []

playQ1 = True
playK1 = True
playQ2 = True
playK2 = True

iWin = None
iLose = None

def load_resources():
    global gameBoards
    global pieceSets
    global soundSets
    global iWin, iLose

    newImage = simplegui.load_image("https://dl.dropboxusercontent.com/u/3381080/chess/board_black.jpg")
    gameBoards.append(newImage)
    newImage = simplegui.load_image("https://dl.dropboxusercontent.com/u/3381080/chess/board_blue.jpg")
    gameBoards.append(newImage)
    newImage = simplegui.load_image("https://dl.dropboxusercontent.com/u/3381080/chess/board_brown.jpg")
    gameBoards.append(newImage)

    newImage = simplegui.load_image("https://dl.dropboxusercontent.com/u/3381080/chess/piece_black.png")
    pieceSets.append(newImage)
    newImage = simplegui.load_image("https://dl.dropboxusercontent.com/u/3381080/chess/piece_blue.png")
    pieceSets.append(newImage)
    newImage = simplegui.load_image("https://dl.dropboxusercontent.com/u/3381080/chess/piece_brown.png")
    pieceSets.append(newImage)
    newImage = simplegui.load_image("https://dl.dropboxusercontent.com/u/3381080/chess/piece_green.png")
    pieceSets.append(newImage)
    newImage = simplegui.load_image("https://dl.dropboxusercontent.com/u/3381080/chess/piece_red.png")
    pieceSets.append(newImage)
    newImage = simplegui.load_image("https://dl.dropboxusercontent.com/u/3381080/chess/piece_violet.png")
    pieceSets.append(newImage)

    iWin = simplegui.load_image("https://dl.dropboxusercontent.com/u/3381080/chess/zyouwin.png")
    iLose = simplegui.load_image("https://dl.dropboxusercontent.com/u/3381080/chess/zyoulose.png")

    newSound = simplegui.load_sound("https://dl.dropboxusercontent.com/u/3381080/chess/sound_playerMove.wav")
    soundSets.append(newSound)
    newSound = simplegui.load_sound("https://dl.dropboxusercontent.com/u/3381080/chess/sound_oponentMove.wav")
    soundSets.append(newSound)
    newSound = simplegui.load_sound("https://dl.dropboxusercontent.com/u/3381080/chess/sound_kingWarning.wav")
    soundSets.append(newSound)
    newSound = simplegui.load_sound("https://dl.dropboxusercontent.com/u/3381080/chess/sound_queenAttention.wav")
    soundSets.append(newSound)
    newSound = simplegui.load_sound("https://dl.dropboxusercontent.com/u/3381080/chess/sound_pieceTaken.wav")
    soundSets.append(newSound)
    newSound = simplegui.load_sound("https://dl.dropboxusercontent.com/u/3381080/chess/sound_gameIntro.wav")
    soundSets.append(newSound)
    newSound = simplegui.load_sound("https://dl.dropboxusercontent.com/u/3381080/chess/sound_gamePause.wav")
    soundSets.append(newSound)
    newSound = simplegui.load_sound("https://dl.dropboxusercontent.com/u/3381080/chess/sound_gameEndEnd.wav")
    soundSets.append(newSound)

    playSound("intro")


def boardType(color):
    if color == "black":
        return gameBoards[0], [440, 440]
    if color == "blue":
        return gameBoards[1], [440, 440]
    if color == "brown":
        return gameBoards[2], [440, 440]
    return gameBoards[0], [440, 440]


def draw_board(canvas, color):
    img, size = boardType(color)
    canvas.draw_image(img, (size[0] // 2, size[1] // 2), (size[0], size[1]), (860 // 2, 860 // 2), (size[0] * 2, size[1] * 2))


def pieceType(color, piece):
    if color == "black":
        return pieceModel(pieceSets[0], piece)
    if color == "blue":
        return pieceModel(pieceSets[1], piece)
    if color == "brown":
        return pieceModel(pieceSets[2], piece)
    if color == "green":
        return pieceModel(pieceSets[3], piece)
    if color == "red":
        return pieceModel(pieceSets[4], piece)
    if color == "violet":
        return pieceModel(pieceSets[5], piece)
    return pieceModel(pieceSets[0], piece)


def pieceModel(imag, piece):
    x = 20
    y = 20

    if piece == "p":
        return imag, [x, y+50]
    if piece == "r":
        return imag, [x, y]
    if piece == "n":
        return imag, [x+50, y]
    if piece == "b":
        return imag, [x+100, y]
    if piece == "q":
        return imag, [x+150, y]
    if piece == "k":
        return imag, [x+200, y]

    x = 20
    y = 320

    if piece == "P":
        return imag, [x, y]
    if piece == "R":
        return imag, [x, y+50]
    if piece == "N":
        return imag, [x+50, y+50]
    if piece == "B":
        return imag, [x+100, y+50]
    if piece == "Q":
        return imag, [x+150, y+50]
    if piece == "K":
        return imag, [x+200, y+50]

    return None


def draw_piece(canvas, color, piece, location):
    imag, imagl = pieceType(color, piece)
    canvas.draw_image(imag, (imagl[0] + 50 // 2, imagl[1] + 50 // 2), (50, 50), (location[0] + 160 // 2, location[1] + 160 // 2), (100, 100))


def draw_piecet(canvas, color, piece, location, number):
    imag, imagl = pieceType(color, piece)
    while number != 0:
        number -= 1
        canvas.draw_image(imag, (imagl[0] + 50 // 2, imagl[1] + 50 // 2), (50, 50), (location[0] + 160 // 2, location[1] + 160 // 2), (50, 50))
        location[0] += 25


def playSound(sound):
    if sound == "pMove":
        soundSets[0].play()
    if sound == "oMove":
        soundSets[1].play()
    if sound == "kingA":
        soundSets[2].play()
    if sound == "queenA":
        soundSets[3].play()
    if sound == "pieceTaken":
        soundSets[4].play()
    if sound == "intro":
        soundSets[5].play()
    if sound == "end1":
        soundSets[6].play()
    if sound == "end2":
        soundSets[7].play()
