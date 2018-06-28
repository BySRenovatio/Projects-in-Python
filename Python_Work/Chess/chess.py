VER = "1.0.1"
DATE = "10/05/2014"
INTERVAL = 20                           # 50 FPS
GAME_W = 1400
GAME_H = 860
BOARD_COLOR = ["black", "blue", "brown"]
PIECE_COLOR = ["black", "blue", "brown", "green", "red", "violet"]
BOARDC = "black"
PIECEC = "blue"

import copy
import random

try:
    import simplegui
except:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

try:
    import resource
except:
    import user32_ab4fxoghQ1XvxyK as resource

try:
    import gameAI
except:
    import user32_BrTscHu21kwbo1U as gameAI


class GameEngine:
    def __init__(self):
        self.pieceSelected = False
        self.pieceSelectedC = [-1, -1]

        self.bot1Activated = False
        self.bot2Activated = True
        self.toMove = 0

        self.p1ticks = 0
        self.p2ticks = 0
        self.TICKS = 0

        self.gameState = 0

        self.moveList = []

        self.x = None
        self.y = None

        self.piecesLeft = 32

        self.drawDirection = 1

        self.mouseUpdated = False

        resource.load_resources()

        self.pos = gameAI.GameState(gameAI.initial, 0, (True, True), (True, True), 0, 0)
        self.posc = None

        self.frame = simplegui.create_frame("Codeskulptor PyChess : @bysorynyos", GAME_W, GAME_H, 0)

        self.frame.set_keydown_handler(self.keydown)
        self.frame.set_mouseclick_handler(self.mouseclick)

        self.frame.set_draw_handler(self.drawHandler)

        timer = simplegui.create_timer(10, self.timerHandler)
        timer.start()

        self.frame.start()

    def timerHandler(self):
        if self.gameState == 0:
            self.TICKS += 1

    def parse(self, c):
        fil, rank = ord(c[0]) - ord('a'), int(c[1]) - 1
        return gameAI.A1 + fil - 10*rank

    def render(self, i):
        rank, fil = divmod(i - gameAI.A1, 10)
        return chr(fil + ord('a')) + str(-rank + 1)

    def getMove(self, cList, x, y):
        p1 = ["a", "8"]
        p2 = ["a", "8"]
        p1[0] = chr(ord('a') + cList[0])
        p1[1] = chr(ord('8') - cList[1])
        p2[0] = chr(ord('a') + x)
        p2[1] = chr(ord('8') - y)
        return self.parse(p1), self.parse(p2)

    def values(self, count):
        if 20 <= count <= 100:
            x = (count - 10) // 10
            y = count % 10
            if 1 <= x <= 8 and 1 <= y <= 9:
                return x - 1, y - 1
        return -1, -1

    def keydown(self, key):
        if key == simplegui.KEY_MAP["space"]:
            self.pos = copy.copy(self.posc)
            self.pieceSelected = False
            self.pieceSelectedC = [-1, -1]
            self.mouseUpdated = False
            self.moveList.pop()
            self.moveList.pop()

    def mouseclick(self, pos):
        global BOARDC, PIECEC

        self.x = pos[0]
        self.y = pos[1]
        self.mouseUpdated = True

        if 865 <= pos[0] <= 1125:
            if 101 <= pos[1] <= 198:
                PIECEC = random.choice(PIECE_COLOR)

        if 1130 <= pos[0] <= 1400:
            if 101 <= pos[1] <= 198:
                BOARDC = random.choice(BOARD_COLOR)

    def drawHandler(self, canvas):
        if self.toMove == 3 and self.gameState == 0:
            # Bot 1 move
            move, score = gameAI.search(self.pos)
            self.moveList.append([self.render(119-move[0]), self.render(119-move[1])])
            if score <= - gameAI.MATE_VALUE:
                self.gameState = 1
            if score >= gameAI.MATE_VALUE:
                self.gameState = 2
            self.pos = self.pos.move(move)
            self.toMove = 2

            if self.drawDirection == 1:
                self.drawDirection = 2
            else:
                self.drawDirection = 1

            self.p1ticks += self.TICKS
            self.TICKS = 0
        elif self.gameState == 0 and self.toMove == 2:
            # Bot 2 move
            move, score = gameAI.search(self.pos)
            self.moveList.append([self.render(119-move[0]), self.render(119-move[1])])
            resource.playSound("oMove")
            if score <= - gameAI.MATE_VALUE:
                self.gameState = 2
            if score >= gameAI.MATE_VALUE:
                self.gameState = 1
            self.pos = self.pos.move(move)

            self.toMove = 0

            if self.bot1Activated is True:
                self.toMove = 3

            if self.drawDirection == 1:
                self.drawDirection = 2
            else:
                self.drawDirection = 1

            self.p2ticks += self.TICKS
            self.TICKS = 0
        elif self.gameState == 0 and self.toMove == 0:
            # Player move
            if 0 <= self.x <= 860:
                if 0 <= self.y <= 860:
                    currentX = (self.x - 30) / 100
                    currentY = (self.y - 30) / 100
                    if 0 <= currentX <= 7 and 0 <= currentY <= 7:
                        if self.pieceSelected is False and self.mouseUpdated is True:
                            self.pieceSelectedC = [currentX, currentY]
                            self.pieceSelected = True
                        elif self.pieceSelected is True:
                            move = self.getMove(self.pieceSelectedC, currentX, currentY)
                            if move in self.pos.genMoves():
                                self.posc = copy.copy(self.pos)
                                self.pos = self.pos.move(move)
                                self.pieceSelected = False
                                self.mouseUpdated = False
                                self.moveList.append([self.render(119-move[0]), self.render(119-move[1])])
                                resource.playSound("pMove")
                                if self.drawDirection == 1:
                                    self.drawDirection = 2
                                else:
                                    self.drawDirection = 1
                                self.toMove = 0
                                if self.bot2Activated is True:
                                    self.toMove = 2

                                self.p1ticks += self.TICKS
                                self.TICKS = 0

        # draw board
        resource.draw_board(canvas, BOARDC)

        # draw pieces
        if self.drawDirection == 1:
            for i, p in enumerate(self.pos.board):
                x, y = self.values(i)
                if p in "prnbqkPRNBQK" and x != -1 and y != -1:
                    resource.draw_piece(canvas, PIECEC, p, [y * 100, x * 100])
        else:
            mcopy = self.pos.board[::-1].swapcase()
            for i, p in enumerate(mcopy):
                x, y = self.values(i)
                if p in "prnbqkPRNBQK" and x != -1 and y != -1:
                    resource.draw_piece(canvas, PIECEC, p, [y * 100, x * 100])

        # draw the piece selected border
        if self.pieceSelected is True:
            p1 = [self.pieceSelectedC[0] * 100 + 30, self.pieceSelectedC[1] * 100 + 30]
            p2 = [p1[0] + 100, p1[1] + 100]
            canvas.draw_polygon([[p1[0], p1[1]], [p1[0], p2[1]], [p2[0], p2[1]], [p2[0], p1[1]]], 5, "White")

        # draw available moves
        nr = 0
        if self.pieceSelected is True:
            for dx in range(8):
                for dy in range(8):
                    move = self.getMove(self.pieceSelectedC, dx, dy)
                    if move in self.pos.genMoves():
                        nr += 1
                        p1 = [dx * 100 + 30, dy * 100 + 30]
                        p2 = [p1[0] + 100, p1[1] + 100]
                        canvas.draw_polygon([[p1[0], p1[1]], [p1[0], p2[1]], [p2[0], p2[1]], [p2[0], p1[1]]], 5, "Blue")
            if nr == 0:
                self.pieceSelected = False
                self.mouseUpdated = False

        # draw the move list
        canvas.draw_polygon([[865, 435], [1400, 435], [1400, 860], [865, 860]], 1, "Gray", "Gray")
        canvas.draw_text('N.  |  White  |  Black  |', [870, 450], 18, 'White')
        canvas.draw_text('N.  |  White  |  Black  |', [1050, 450], 18, 'White')
        canvas.draw_text('N.  |  White  |  Black  |', [1230, 450], 18, 'White')
        nr = len(self.moveList)
        count = -1
        x = 915
        y = 475
        while (count + 1 < nr):
            count += 1
            if count % 2 == 0:
                canvas.draw_text(str(count // 2 + 1), [x - 40, y], 14, 'Red')
                canvas.draw_text(self.moveList[count][0] + " " + self.moveList[count][1], [x, y], 14, 'White')
            else:
                canvas.draw_text(self.moveList[count][0] + " " + self.moveList[count][1], [x + 65, y], 14, 'Black')
                y += 20
                if count == 39 or count == 79:
                    x += 180
                    y = 475

        # draw the pieces taken
        if self.drawDirection == 2:
            mcopy = self.pos.board[::-1].swapcase()
        else:
            mcopy = self.pos.board[:]
        canvas.draw_polygon([[865, 200], [1400, 200], [1400, 430], [865, 430]], 1, "Red", "Red")
        canvas.draw_text('Pieces taken by White', [900, 220], 20, 'White')
        canvas.draw_text('Pieces taken by Black', [1200, 220], 20, 'Black')
        pieces = [[0, 0, 8], [0, 0, 2], [0, 0, 2], [0, 0, 2], [0, 0, 1], [0, 0, 1]]
        howmany = 0
        for i, p in enumerate(mcopy):
            if p == 'p':
                pieces[0][0] += 1
                howmany += 1
            elif p == 'P':
                pieces[0][1] += 1
                howmany += 1
            elif p == 'r':
                pieces[1][0] += 1
                howmany += 1
            elif p == 'R':
                pieces[1][1] += 1
                howmany += 1
            elif p == 'n':
                pieces[2][0] += 1
                howmany += 1
            elif p == 'N':
                pieces[2][1] += 1
                howmany += 1
            elif p == 'b':
                pieces[3][0] += 1
                howmany += 1
            elif p == 'B':
                pieces[3][1] += 1
                howmany += 1
            elif p == 'q':
                pieces[4][0] += 1
                howmany += 1
            elif p == 'Q':
                pieces[4][1] += 1
                howmany += 1
            elif p == 'k':
                pieces[5][0] += 1
                howmany += 1
            elif p == 'K':
                pieces[5][1] += 1
                howmany += 1

        if self.piecesLeft != howmany:
            resource.playSound("pieceTaken")
            self.piecesLeft = howmany

        # draw pawns
        if pieces[0][0] != pieces[0][2]:
            resource.draw_piecet(canvas, PIECEC, 'p', [825, 180], pieces[0][2] - pieces[0][0])
        if pieces[0][1] != pieces[0][2]:
            resource.draw_piecet(canvas, PIECEC, 'P', [825 + 300, 180], pieces[0][2] - pieces[0][1])
        # draw rocks
        if pieces[1][0] != pieces[1][2]:
            resource.draw_piecet(canvas, PIECEC, 'r', [825, 240], pieces[1][2] - pieces[1][0])
        if pieces[1][1] != pieces[1][2]:
            resource.draw_piecet(canvas, PIECEC, 'R', [825 + 300, 240], pieces[1][2] - pieces[1][1])
        # draw knights
        if pieces[2][0] != pieces[2][2]:
            resource.draw_piecet(canvas, PIECEC, 'n', [875, 240], pieces[2][2] - pieces[2][0])
        if pieces[2][1] != pieces[2][2]:
            resource.draw_piecet(canvas, PIECEC, 'N', [875 + 300, 240], pieces[2][2] - pieces[2][1])
        # draw bishops
        if pieces[3][0] != pieces[3][2]:
            resource.draw_piecet(canvas, PIECEC, 'b', [925, 240], pieces[3][2] - pieces[3][0])
        if pieces[3][1] != pieces[3][2]:
            resource.draw_piecet(canvas, PIECEC, 'B', [925 + 300, 240], pieces[3][2] - pieces[3][1])
        # draw queens
        if pieces[4][0] != pieces[4][2]:
            resource.draw_piecet(canvas, PIECEC, 'q', [825, 300], pieces[4][2] - pieces[4][0])
            if resource.playQ1 is True:
                resource.playSound("queenA")
            resource.playQ1 = False
        if pieces[4][1] != pieces[4][2]:
            resource.draw_piecet(canvas, PIECEC, 'Q', [825 + 300, 300], pieces[4][2] - pieces[4][1])
            if resource.playQ2 is True:
                resource.playSound("queenA")
            resource.playQ2 = False
        #draw king
        if pieces[5][0] != pieces[5][2]:
            resource.draw_piecet(canvas, PIECEC, 'k', [875, 300], pieces[5][2] - pieces[5][0])
            if resource.playK1 is True:
                resource.playSound("kingA")
            resource.playK1 = False
        if pieces[5][1] != pieces[5][2]:
            resource.draw_piecet(canvas, PIECEC, 'K', [875 + 300, 300], pieces[5][2] - pieces[5][1])
            if resource.playK2 is True:
                resource.playSound("kingA")
            resource.playK2 = False

        # draw the change color stuff
        canvas.draw_text('Change Piece color: ' + PIECEC, [880, 150], 20, 'White')
        canvas.draw_polygon([[865, 101], [1125, 101], [1125, 198], [865, 198]], 3, PIECEC)
        canvas.draw_text('Change Board color: ' + BOARDC, [1140, 150], 20, 'White')
        canvas.draw_polygon([[1130, 101], [1400, 101], [1400, 198], [1130, 198]], 3, BOARDC)

        # draw the bot settings
        if self.bot2Activated is False:
            canvas.draw_polygon([[0, 0], [0, 30], [30, 30], [30, 0]], 1, "White", "White")
        else:
            canvas.draw_polygon([[0, 0], [0, 30], [30, 30], [30, 0]], 1, "Red", "Red")
        if self.bot1Activated is False:
            canvas.draw_polygon([[0, 830], [30, 830], [30, 860], [0, 860]], 1, "White", "White")
        else:
            canvas.draw_polygon([[0, 830], [30, 830], [30, 860], [0, 860]], 1, "Red", "Red")

        # display time spent on moves
        canvas.draw_text('Player1 spent: ' + str(self.p1ticks / 100) + ' seconds', [880, 30], 20, 'White')
        canvas.draw_text('Player2 spent: ' + str(self.p2ticks / 100) + ' seconds', [1140, 30], 20, 'White')
        canvas.draw_text('Current move: ' + str(self.TICKS / 100) + ' seconds', [1010, 70], 25, 'White')

        if self.gameState == 2:
            canvas.draw_image(resource.iWin, (1184 // 2, 732 // 2), (1184, 732), (1400 // 2, 860 // 2), (1184 // 2, 732 // 2))
            resource.playSound("end1")
        if self.gameState == 1:
            canvas.draw_image(resource.iLose, (489 // 2, 483 // 2), (489, 483), (1400 // 2, 860 // 2), (489, 483))
            resource.playSound("end2")

# Start the game
newGame = GameEngine()

