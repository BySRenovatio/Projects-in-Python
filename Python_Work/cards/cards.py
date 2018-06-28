# Mini-project #6 - Blackjack
import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)

    def drawBack(self, canvas, pos):
        card_loc = (CARD_BACK_CENTER[0], CARD_BACK_CENTER[1])
        canvas.draw_image(card_back, card_loc, CARD_BACK_SIZE, [pos[0] + CARD_BACK_CENTER[0] + 1, pos[1] + CARD_BACK_CENTER[1] + 1], CARD_BACK_SIZE)

# define hand class
class Hand:
    def __init__(self):
        # create Hand object
        self.cards = []

    def __str__(self):
        # return a string representation of a hand
        stringCards = ""
        for card in self.cards:
            stringCards = stringCards + str(card) + " "
        return "Hand contains " + stringCards.strip()
        # remove the space from the end of the string

    def add_card(self, card):
        # add a card object to a hand
        self.cards.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        nValue = 0
        bAce = False
        for card in self.cards:
            nValue += VALUES[card.get_rank()]
            if card.get_rank() == 'A':
                bAce = True
        # value not exceeding 21 then count it as a ten
        if bAce and nValue < 12:
            nValue += 10
        return nValue

    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        for card in self.cards:
            pos[0] = pos[0] + CARD_SIZE[0] + 20
            card.draw(canvas, pos)

# define deck class
class Deck:
    def __init__(self):
        # create a Deck object
        self.cards = []
        for suit in SUITS:
            for rank in RANKS:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        # shuffle the deck
        # use random.shuffle()
        random.shuffle(self.cards)

    def deal_card(self):
        # deal a card object from the deck
        return self.cards.pop()

    def __str__(self):
        # return a string representing the deck
        stringCards = ""
        for card in self.cards:
            stringCards = stringCards + str(card) + " "
        return "Deck contains " + stringCards.strip()

#define event handlers for buttons
def deal():
    global outcome, in_play
    global dDeck, pPlayer, dDealer, sPlayer, sDealer
    global score, sMessage

    if in_play:
        score -= 1
        in_play = False
        deal()
    else:
        dDeck = Deck()
        pPlayer = Hand()
        dDealer = Hand()
        dDeck.shuffle()
        pPlayer.add_card(dDeck.deal_card())
        pPlayer.add_card(dDeck.deal_card())
        dDealer.add_card(dDeck.deal_card())
        dDealer.add_card(dDeck.deal_card())
        outcome = "Hit or Stand?"
        sPlayer = "Player"
        sDealer = "Dealer"
        sMessage = ""
        in_play = True

def hit():
    global in_play, score, outcome
    global dDeck, pPlayer
    global sPlayer, sMessage

    # if the hand is in play, hit the player
    # if busted, assign a message to outcome, update in_play and score

    if in_play:
        if pPlayer.get_value() < 22:
            pPlayer.add_card(dDeck.deal_card())
            if pPlayer.get_value() > 21:
                sPlayer = "Busted!"
                sMessage = "You've busted! You loose!"
                score -= 1
                outcome = "New deal?"
                in_play = False

def stand():
    global in_play, score, outcome
    global dDealer, pPlayer
    global sDealer, sMessage

    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    # assign a message to outcome, update in_play and score
    if in_play:
        while (dDealer.get_value() < 17):
            dDealer.add_card(dDeck.deal_card())
        if dDealer.get_value() > 21:
            sDealer = "Busted!"
            sMessage = "Dealer busted! You win!"
            score += 1
            outcome = "New deal?"
            in_play = False
        elif pPlayer.get_value() > dDealer.get_value():
            sMessage = "Your hand's stronger! You win!"
            score += 1
            outcome = "New deal?"
            in_play = False
        else:
            sMessage = "Your hand's weaker! You loose!"
            score -= 1
            outcome = "New deal?"
            in_play = False

def draw(canvas):
    # draw handler
    canvas.draw_text("Blackjack", (60, 100), 40, "Aqua")
    canvas.draw_text(sDealer, (60, 185), 33, "Black")
    canvas.draw_text(sPlayer, (60, 385), 33, "Black")
    canvas.draw_text(outcome, (250, 385), 33, "Black")
    canvas.draw_text(sMessage, (250, 185), 25, "Black")
    canvas.draw_text("Score: " + str(score), (450, 100), 33, "Black")
    dDealer.draw(canvas, [-65, 200])
    pPlayer.draw(canvas, [-65, 400])
    if in_play:
        dDealer.cards[0].drawBack(canvas, [28, 200])

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()