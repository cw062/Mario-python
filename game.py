import pygame
import time

from pygame.locals import*
from time import sleep

class Model():
	def __init__(self):
		self.MARIO = 0
		self.TUBE = 1
		self.GOOMBA = 2
		self.FIREBALL = 3
		self.isOnASprite = False
		self.sprList = []
		self.marioArr = []
		self.tubeArr = []
		self.goombaArr = []
		self.fireballArr = []
		self.sprList.append(self.marioArr)
		self.sprList.append(self.tubeArr)
		self.sprList.append(self.goombaArr)
		self.sprList.append(self.fireballArr)
		self.sprList[self.MARIO].append(Mario(100,355))
		self.sprList[self.TUBE].append(Tube(300, 350))
		self.sprList[self.TUBE].append(Tube(700, 330))
		self.sprList[self.TUBE].append(Tube(900, 330))
		self.sprList[self.TUBE].append(Tube(1200, 330))
		self.sprList[self.GOOMBA].append(Goomba(400, 300))
		self.sprList[self.GOOMBA].append(Goomba(800, 300))

	def update(self):
		isMarioCollinding = False
		collided = False
		self.sprList[self.MARIO][self.MARIO].savePrevCoord()
		#mario up and down collision
		for r in range(len(self.sprList)):
			c = 0
			for sprtie in self.sprList[r]:
				if r == self.TUBE or r == self.GOOMBA:
					isMarioCollinding = self.collision(r, c, self.MARIO)
					if isMarioCollinding:
						collided = isMarioCollinding
						self.sprList[self.MARIO][self.MARIO].y = self.sprList[r][c].y - self.sprList[self.MARIO][self.MARIO].height
				c += 1
		self.sprList[self.MARIO][self.MARIO].update(collided)
		if self.sprList[self.MARIO][self.MARIO].y == 355 or collided:
			self.sprList[self.MARIO][self.MARIO].framesInAir = 0
			self.sprList[self.MARIO][self.MARIO].isFalling = False
		self.updateGoomba()
		indexf = 0
		indexg = 0
		counterg = 0
		counterf = 0
		for f in self.sprList[self.FIREBALL]:
			f.shoot()
			for g in self.sprList[self.GOOMBA]:
				point_x = f.x + f.width
				point_y = f.y + f.height
				if point_x >= g.x and point_x <= g.x + g.width and point_y >= g.y and point_y <= g.y + g.height:
					g.updateImage()

	def updateGoomba(self):
		for g in self.sprList[self.GOOMBA]:
			for t in self.sprList[self.TUBE]:
				if g.x <= t.x + t.width and g.x + g.width > t.x + t.width:
					g.direction = 3
				elif g.x + g.width >= t.x and g.x < t.x:
					g.direction = -3
			g.update()

	def collision(self, row, col, sprCol):
		left =  self.sprList[row][col].x 
		right = self.sprList[row][col].x + self.sprList[row][col].width
		bottom = self.sprList[row][col].y + self.sprList[row][col].height
		top = self.sprList[row][col].y
		for sprRow in range(len(self.sprList)):
			if self.sprList[sprRow][sprCol].x > right:
				return False
			elif self.sprList[sprRow][sprCol].x + self.sprList[sprRow][sprCol].width < left:
				return False
			elif self.sprList[sprRow][sprCol].y > bottom:
				return False
			elif self.sprList[sprRow][sprCol].y + self.sprList[sprRow][sprCol].height < top:
				return False
			else:
				return True
class View():
	def __init__(self, model):
		screen_size = (1000,600)
		self.screen = pygame.display.set_mode(screen_size, 32)
		self.model = model
		self.model.rect = self.model.sprList[0][0].image.get_rect()
	def update(self):
		sky = (0, 191, 255)
		ground = (126, 240, 80)
		pygame.draw.rect(self.screen, sky, (0,0,1000, 450), 0) 
		pygame.draw.rect(self.screen, ground, (0,450,1000,150), 0)
		for row in range(len(self.model.sprList)):
			for col in range(len(self.model.sprList[row])):
				self.screen.blit(self.model.sprList[row][col].image, (self.model.sprList[row][col].x, self.model.sprList[row][col].y))
		pygame.display.flip()

class Controller():
	def __init__(self, model):
		self.model = model
		self.keep_going = True

	def update(self):
		for event in pygame.event.get():
			if event.type == QUIT:
				self.keep_going = False
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE: 
					self.keep_going = False
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_UP:
					self.model.sprList[self.model.MARIO][self.model.MARIO].isFalling = True
				elif event.key == pygame.K_SPACE:
					self.model.sprList[self.model.MARIO][self.model.MARIO].isFalling = True
		keys = pygame.key.get_pressed()
		if keys[K_LEFT]:
			for row in range(len(self.model.sprList)):
				for col in range(len(self.model.sprList[row])):
					if row > 0:
						self.model.sprList[row][col].savePrevCoord()
						self.model.sprList[row][col].x += 5
						if not row == self.model.FIREBALL:
							if self.model.collision(row, col, 0) and self.model.sprList[0][0].y + self.model.sprList[0][0].height != self.model.sprList[row][col].y:
								for i in range(len(self.model.sprList)):
									for j in range(len(self.model.sprList[i])):
										if i > 0:
											self.model.sprList[i][j].x = self.model.sprList[i][j].px
			self.model.sprList[self.model.MARIO][self.model.MARIO].updateImage()
		if keys[K_RIGHT]:
			for row in range(len(self.model.sprList)):
				for col in range(len(self.model.sprList[row])):
					if row > 0:
						self.model.sprList[row][col].savePrevCoord()
						self.model.sprList[row][col].x -= 5
						if not row == self.model.FIREBALL:
							if self.model.collision(row, col, 0) and self.model.sprList[0][0].y + self.model.sprList[0][0].height != self.model.sprList[row][col].y:
								for i in range(len(self.model.sprList)):
									for j in range(len(self.model.sprList[i])):
										if i > 0:
											self.model.sprList[i][j].x = self.model.sprList[i][j].px
			self.model.sprList[self.model.MARIO][self.model.MARIO].updateImage()
		if keys[K_UP]:
			if self.model.sprList[self.model.MARIO][self.model.MARIO].framesInAir < 20 and not self.model.sprList[self.model.MARIO][self.model.MARIO].isFalling:
				self.model.sprList[self.model.MARIO][self.model.MARIO].savePrevCoord()
				self.model.sprList[self.model.MARIO][self.model.MARIO].y -= 20
				self.model.sprList[self.model.MARIO][self.model.MARIO].framesInAir += 1
		if keys[K_SPACE]:
			if self.model.sprList[self.model.MARIO][self.model.MARIO].framesInAir < 20 and not self.model.sprList[self.model.MARIO][self.model.MARIO].isFalling:
				self.model.sprList[self.model.MARIO][self.model.MARIO].savePrevCoord()
				self.model.sprList[self.model.MARIO][self.model.MARIO].y -= 20
				self.model.sprList[self.model.MARIO][self.model.MARIO].framesInAir += 1
		if keys[K_LCTRL] or keys[K_RCTRL]:
			self.model.sprList[self.model.FIREBALL].append(Fireball(self.model.sprList[self.model.MARIO][self.model.MARIO].x, self.model.sprList[self.model.MARIO][self.model.MARIO].y))

class Sprite():
	def __init__(self, x, y, width, height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height

	def savePrevCoord(self):
		self.px = self.x
		self.py = self.y

class Mario(Sprite):
	def __init__(self, x, y):
		Sprite.__init__(self, x, y, 60, 95)
		self.marioImages = [pygame.image.load("mario1.png"), pygame.image.load("mario2.png"),
		pygame.image.load("mario3.png"), pygame.image.load("mario4.png"), pygame.image.load("mario5.png")]
		self.imageNum = 0
		self.image = self.marioImages[self.imageNum]
		self.framesInAir = 0
		self.isFalling = False

	def update(self, isCollinding):
		if not isCollinding:
			self.y += 7
		if self.y + 95 > 450:
			self.y = 355

	def updateImage(self):
		if self.imageNum < 4:
			self.imageNum += 1
		else:
			self.imageNum = 0
		self.image = self.marioImages[self.imageNum]

class Tube(Sprite):
	def __init__(self, x, y):
		Sprite.__init__(self, x, y, 55, 272)
		self.image = pygame.image.load("tube.png")

class Goomba(Sprite):
	def __init__(self, x, y):
		Sprite.__init__(self, x, y, 50, 60)
		self.goombaImages = [pygame.image.load("goomba.png"), pygame.image.load("goomba_fire.png")]
		self.imageNum = 0
		self.image = self.goombaImages[self.imageNum]
		self.direction = 3
		self.willDie = 0

	def update(self):
		if self.y + self.height < 450:
			self.y += 5
		if self.y + self.height > 450:
			self.y = 390
		self.x += self.direction
		if self.willDie > 0:
			self.willDie += 1

	def updateImage(self):
		self.imageNum = 1
		self.image = self.goombaImages[self.imageNum]

class Fireball(Sprite):
	def __init__(self, x, y):
		Sprite.__init__(self, x + 55, y + 10, 47, 47)
		self.image = pygame.image.load("fireball.png")
		self.px = self.x +55
		self.py = self.y + 10
		self.direction = 0

	def shoot(self):
		if self.y >= 403:
			self.direction = 1
		if self.y < 403 and self.direction == 0:
			self.x += 5
			self.y += 3
		elif self.direction == 1:
			self.y -= 6
			self.x += 5

print("Use the arrow keys to move. Press Esc to quit.")
pygame.init()
m = Model()
v = View(m)
c = Controller(m)
while c.keep_going:
	c.update()
	m.update()
	v.update()
	sleep(0.04)