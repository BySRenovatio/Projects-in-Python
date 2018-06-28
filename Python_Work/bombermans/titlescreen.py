import sys, pygame, config, game, highscore

class Titlescreen():

	def __init__(self):
		self.c = config.Config()
		exitMain = False

		while not exitMain:
			pygame.init()
			self.screen = pygame.display.set_mode((1028,768))
			pygame.display.set_caption("Bomberman")

			clock = pygame.time.Clock()
			pygame.mouse.set_visible(True)
			pygame.display.flip()
			userInteracted = False

			while not userInteracted:
				clock.tick(self.c.FPS)
				self.singlePlayer() # Single Player game clicked

	def withinBoundary(self, x1, x2, y1, y2):
		if pygame.mouse.get_pos()[0] >= x1 and pygame.mouse.get_pos()[0] <= x2 and pygame.mouse.get_pos()[1] >= y1 and pygame.mouse.get_pos()[1] <= y2:
			return True
		return False

	def singlePlayer(self):
		g = game.Game(self.c.SINGLE)

	def multiplayer(self):
		g = game.Game(self.c.MULTI)

	def instructions(self):
		print "Instructions clicked!"

	def highScores(self):
		h = highscore.Highscore()
		h.displayScore()

	def clearBackground(self):
		bg = pygame.Surface(self.screen.get_size())
		bg = bg.convert()
		bg.fill((0,0,0))
		self.blit(bg,(0,0))

if __name__ == "__main__":
    t = Titlescreen()
