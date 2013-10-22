#!/usr/bin/env python
# an obstacle and enemy avoidance platformer

from cPickle import dump, load
from sys import exit
from os import path, environ
from random import randint, choice
import pygame
from pygame.locals import *
from pygame.color import THECOLORS as color

class CloudSprite(pygame.sprite.DirtySprite):
	image = None
	def __init__(self, scriptpath, pos):
		self.dirty = True
		pygame.sprite.DirtySprite.__init__(self)
		if CloudSprite.image == None:
			CloudSprite.image = pygame.image.load(path.join(scriptpath, 'assets', 'cloud.png')).convert_alpha()
		self.image = CloudSprite.image
		self.rect = pygame.Rect(pos[0], pos[1], self.image.get_width(), self.image.get_height())
		self.speed = 2
		self.dir = 0

	def update(self):
		self.dirty = True
		if self.rect.left <= 800:
			self.rect.left += self.speed
		else:
			self.rect.x = -self.image.get_width()


class PlayerSprite(pygame.sprite.DirtySprite):
	def __init__(self, scriptpath, pos, screen_width):
		self.dirty = True
		pygame.sprite.DirtySprite.__init__(self)
		self.image = pygame.image.load(path.join(scriptpath, 'assets', 'Character Boy2.png')).convert_alpha()
		self.rect = pygame.Rect(pos[0], pos[1], self.image.get_width(), self.image.get_height())
		self.screen_width = screen_width
		self.y = pos[1]
		self.speed = 8
		self.l, self.r = False, False
		self.jstep1, self.jstep2 = False, False
		self.jumpheight = 160 #200
		self.gravity = 15
		self.topofwall = False
		self.newy = None
		self.mask = pygame.mask.from_surface(self.image)

	def update(self):
		self.dirty = True
		if self.l and self.rect.left > 0 + self.speed:
			self.rect.left -= self.speed
		elif self.r: #and self.rect.right < self.screen_width - self.speed:
			self.rect.right += self.speed
		if self.jstep1:
			if self.rect.y > self.newy - self.jumpheight: #self.y - self.jumpheight:
				self.rect.y -= self.gravity
			else:
				self.jstep1 = False
				self.jstep2 = True
		elif self.jstep2:
			if self.rect.y < self.y: #- self.gravity < self.y:
				self.rect.y += self.gravity
			if self.rect.y == self.y:
				self.jstep1 = False
				self.jstep2 = False


class MountainLayer(pygame.sprite.DirtySprite):
	def __init__(self, surface, screen_width, pos):
		self.dirty = True
		pygame.sprite.DirtySprite.__init__(self)
		self.image = surface
		self.rect = pygame.Rect(pos[0], pos[1], self.image.get_width(), self.image.get_height())
		self.start = pos
		self.screen_width = screen_width
		self.speed = 1
		self.l, self.r = False, False

	def update(self):

		if self.rect.x >= 0:
			self.rect.x = self.start[0]
		if self.rect.right <= self.screen_width:
			self.rect.x = self.start[0]
		if self.r:
			self.rect.left += self.speed
			self.dirty = True
		elif self.l:
			self.rect.left -= self.speed
			self.dirty = True


class Barrier1(pygame.sprite.DirtySprite):
	image = None
	def __init__(self, scriptpath, pos):
		self.dirty = False
		pygame.sprite.DirtySprite.__init__(self)
		if Barrier1.image == None:
			Barrier1.image = pygame.image.load(path.join\
			(scriptpath, 'assets', 'block.png')).convert()
		self.rect = pygame.Rect(pos[0], pos[1], 32, 32)
		self.mask = pygame.mask.from_surface(self.image)


#	def update(self):
#		self.dirty = False


class Money(pygame.sprite.DirtySprite):
	image = None
	def __init__(self, scriptpath, pos):
		self.dirty = False
		pygame.sprite.DirtySprite.__init__(self)
		if Money.image == None:
			Money.image = pygame.image.load(path.join(scriptpath, \
			'assets', 'money2.png')).convert_alpha()
		self.rect = pygame.Rect(pos[0], pos[1], 32, 32)


class FlyingEnemy(pygame.sprite.DirtySprite):
	image = None
	def __init__(self, scriptpath, pos):
		self.dirty = True
		pygame.sprite.DirtySprite.__init__(self)
		if FlyingEnemy.image == None:
			FlyingEnemy.image = pygame.image.load(path.join(scriptpath,\
			'assets', 'EnemyBird.png')).convert_alpha()
		self.rect = pygame.Rect(pos[0], pos[1], 60, 70)
		self.speed = 4
		self.dir = 0
		self.mask = pygame.mask.from_surface(self.image)

	def update(self):
		self.dirty = True
		if self.rect.right >= 0:
			self.rect.right -= self.speed
		else:
			self.rect.x = 800


class GroundEnemy(pygame.sprite.DirtySprite):
	image = None
	def __init__(self, scriptpath, pos):
		self.dirty = True
		pygame.sprite.DirtySprite.__init__(self)
		if GroundEnemy.image == None:
			GroundEnemy.image = pygame.image.load(path.join(scriptpath,\
			'assets', 'Bug.png')).convert_alpha()
		self.rect = pygame.Rect(pos[0], pos[1], 70, 54)
		self.speed = 2
		self.dir = 0
		self.mask = pygame.mask.from_surface(self.image)

	def update(self):
		self.dirty = True
		if self.rect.right >= 0:
			self.rect.right -= self.speed
		else:
			self.rect.x = 800


class VerticalEnemy(pygame.sprite.DirtySprite):
	image1, image, imageDown, mask1, mask2 = None, None, None, None, None
	def __init__(self, scriptpath, pos):
		self.dirty = True
		pygame.sprite.DirtySprite.__init__(self)
		if VerticalEnemy.image == None:
			VerticalEnemy.image1 = pygame.image.load(path.join(scriptpath,\
			'assets', 'Fish.png')).convert_alpha()
			VerticalEnemy.image = VerticalEnemy.image1
		if VerticalEnemy.imageDown == None:
			VerticalEnemy.imageDown = pygame.image.load(path.join(scriptpath,\
			'assets', 'FishDown.png')).convert_alpha()
		if VerticalEnemy.mask1 == None:
			VerticalEnemy.mask1 = pygame.mask.from_surface(VerticalEnemy.image)
		if VerticalEnemy.mask2 == None:
			VerticalEnemy.mask2 = pygame.mask.from_surface(VerticalEnemy.imageDown)
		self.rect = pygame.Rect(pos[0], pos[1], 40, 80)
		self.speed = randint(5,10)
		self.mask = self.mask1
		self.dir = 1
		self.jheight = randint(50,100)

	def update(self):
		self.dirty = True
		if self.dir:
			if self.rect.top >= self.jheight: #100:
				self.rect.top -= self.speed
			else:
				self.dir = 0
		else:
			self.image = self.imageDown
			self.mask = self.mask2
			self.rect.top += self.speed
			if self.rect.bottom >= 330:
				self.dir = 1
				self.image = self.image1
				self.mask = self.mask1


class ScoreField(pygame.sprite.DirtySprite):
	def __init__(self, score, font, tip):
		self.dirty = 1
		pygame.sprite.DirtySprite.__init__(self)
		self.font, self.score, self.tip = font, score, tip
		self.rect = pygame.Rect(5, 372, 770, 25)
		self.image = pygame.Surface((self.rect.width, self.rect.height))
		self.image.fill(color['lightblue'])

	def update(self):
		self.dirty = 1
		self.image.fill(color['lightblue'])
		self.scoretext = self.font.render('Score: %s.  ' % self.score + self.tip, \
		True, color['black'])
		self.image.blit(self.scoretext, (0,0))


def stagemanager(x, y, bg, Width, Height, stage, blocksize, blocks):
	'''Loads new stages'''
# !!! Instead of clearing and blitting to the screen, clear the bg and
# blit the map tiles to it!!!
	bg.fill(color['lightblue'])

	for row in stage:
		for tile in row:
			bg.blit(blocks[tile], (x, y, blocksize[0], blocksize[1]))
			x += blocksize[0]
		y += (blocksize[1] - 30)
		x = 0

	bg.fill(color['lightblue'], Rect(0, 370, 800, 400))


def obstaclemanager(walls, scriptpath):
	'''Loads obstacles'''
	walllist = []
	wallHeight, wallWidth = 32, 32
	walllocations = []

	traplist = []
	traplocations = []

	moneylist = []
	moneylocations = []

	fenemylist = []
	fenemylocations = []

	genemylist = []
	genemylocations = []

	venemylist = []
	venemylocations = []

	x = 96 #100
	y = 8 #72 #104
	locationtypes = (walllocations, moneylocations, traplocations, \
	fenemylocations, genemylocations, venemylocations)

	for row in walls:
		for thing in row:
			if thing:
				locationtypes[thing - 1].append((x,y))
			x += wallWidth
		y += wallHeight
		x = 96 #100

	for pos in walllocations:
		walllist.append(Barrier1(scriptpath, pos))

	for pos in traplocations:
		traplist.append(Barrier1(scriptpath, pos))

	for pos in moneylocations:
		moneylist.append(Money(scriptpath, pos))

	for pos in fenemylocations:
		fenemylist.append(FlyingEnemy(scriptpath, pos))

	for pos in genemylocations:
		genemylist.append(GroundEnemy(scriptpath, pos))

	for pos in venemylocations:
		venemylist.append(VerticalEnemy(scriptpath, pos))

	enemylist = [fenemylist, genemylist, venemylist]
	return walllist, traplist, moneylist, enemylist


def centertext(text, screen):
	textrect = text.get_rect()
	textrect.centerx = screen.get_rect().centerx
	textrect.centery = screen.get_rect().centery
	return textrect


def main():
	pygame.init()
	environ['SDL_VIDEO_CENTERED'] = '1'
	pygame.display.set_caption('Super Meenu')
	Width = 800
	Height = 400
	pygame.mouse.set_visible(0)
	scriptpath = path.dirname(__file__)
	screen = pygame.display.set_mode((Width, Height))
	font = pygame.font.Font(None, 32)
	linespace = pygame.font.Font.get_linesize(font)
	scorefile = path.join(scriptpath, 'assets', 'scores.data')
	splash = pygame.mixer.Sound(path.join(scriptpath, 'assets', 'splash.ogg'))
	jump = pygame.mixer.Sound(path.join(scriptpath, 'assets', 'jump.ogg'))
	money = pygame.mixer.Sound(path.join(scriptpath, 'assets', 'money.ogg'))
	pygame.mixer.music.load(path.join(scriptpath, 'assets', 'music.ogg'))
	pygame.mixer.music.play(-1, 0.0)

	intro = font.render("Help Meenu collect enough money to buy a new iPhone!!!", True, \
	color['black'])
	textrect = centertext(intro, screen)
	screen.fill(color['lightblue'])
	screen.blit(intro, textrect)
	pygame.display.update()
	pygame.time.wait(3000)

# Declare images to load for tiles in images dict, then load, convert
# scale and cache them
# This could be made a function to load different images for different
# levels
# Maybe embed this inside actual Mountain/Backdrop class?
	images = {'grass':'Grass Block.png', 'dirt':'Dirt Block.png', 'water':'Water Block.png'}
	for name in images.keys():
		images[name] = pygame.image.load(path.join(scriptpath,'assets', images[name])).convert()
		images[name] = pygame.transform.scale(images[name], (Width / 8, Height / 4))

	clock = pygame.time.Clock()

# Stages. First number is level, second is stage of that level
# 0 is dirt, 1 is grass, 3 is water
	level = 1
	stage11 = [[1,1,1,1,1,1,1,1],
			   [1,1,1,1,1,1,1,1]]
	stage12 = [[1,1,1,1,1,1,1,1],
			   [1,1,0,1,1,1,1,1]]
	stage13 = [[1,1,1,1,0,1,1,1],
			   [1,1,0,1,1,1,1,1]]
	stage14 = [[1,1,1,1,0,1,1,1],
			   [1,1,0,0,1,1,1,1]]
	stage15 = [[1,0,3,3,3,3,0,1],
			   [1,0,3,3,3,3,0,1]]
	stage16 = [[0,0,3,3,3,3,1,0],
			   [1,0,3,3,3,3,0,0]]
	stage17 = [[0,0,1,0,1,0,1,0],
			   [1,0,0,1,0,0,1,1]]
	stage18 = [[0,0,3,3,3,3,3,3],
			   [0,0,3,3,3,3,3,3]]
	stage19 = [[0,0,3,3,0,0,0,0],
			   [0,0,3,3,1,0,0,0]]
	stage110 = [[0,0,0,0,0,0,0,0],
			    [0,0,0,0,0,0,0,0]]

############
# 0 is empty, 1 is barrier, 2 is gold, 3 is trap, 4 is flying enemy
# 5 is ground enemy, 6 is jumping enemy
###########

	walls11 = ((0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
			   (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
			   (0,0,0,0,0,0,0,0,0,1,0,0,2,0,0,0,0,0,0,0,0,0),
			   (0,0,0,0,0,0,0,2,0,1,0,0,2,0,0,0,0,0,0,0,0,0),
			   (0,0,0,0,0,0,0,1,0,1,0,0,2,0,0,0,0,0,0,0,0,0),
			   (0,0,0,0,0,1,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0),
			   (0,0,0,0,0,1,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0),
			   (0,0,0,1,0,1,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0),
			   (0,0,0,1,0,1,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0),
			   (0,0,0,1,0,1,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0))

	walls12 = ((0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
			   (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
			   (0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0),
			   (0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0),
			   (0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,1,0,0,0,0,0,0),
			   (0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,1,0,0,0,0,0,0),
			   (0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0),
			   (0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0),
			   (0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0),
			   (0,0,0,0,0,0,1,0,0,1,0,0,0,0,2,1,0,0,5,0,0,0))

	walls13 = ((0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
			   (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
			   (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0),
			   (0,0,0,0,0,0,1,0,0,0,0,1,1,1,1,0,0,0,1,0,0,0),
			   (0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0),
			   (0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0),
			   (0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0),
			   (0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0),
			   (0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0),
			   (0,0,0,0,0,0,1,0,5,0,0,0,2,0,0,0,0,5,1,0,0,0))


	walls14 = ((1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
			   (1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
			   (1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
			   (1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
			   (1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
			   (1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
			   (0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
			   (0,0,0,0,0,0,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
			   (0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
			   (0,0,0,0,0,0,0,1,0,0,5,0,0,0,5,0,0,0,5,0,0,0))

	walls15 = ((0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
			   (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
			   (0,0,0,0,0,0,0,0,0,2,2,2,0,0,0,0,0,0,4,0,0,0),
			   (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
			   (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
			   (0,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
			   (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
			   (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
			   (0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0),
			   (0,0,0,0,3,3,3,3,3,3,3,3,1,3,3,0,0,0,0,0,0,0))

	walls16 = ((0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
			   (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
			   (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0),
			   (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
			   (0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
			   (0,0,0,1,0,0,0,1,0,0,0,4,0,0,0,0,0,0,0,0,0,0),
			   (0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0),
			   (0,0,0,1,0,0,0,1,0,0,0,2,0,0,0,1,0,0,0,0,0,0),
			   (0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,0),
			   (0,0,0,1,3,3,3,3,3,3,3,3,3,3,3,1,0,0,0,0,0,0))

	walls17 = ((0,0,0,0,0,4,0,4,0,4,0,0,0,0,0,0,0,0,0,0,0,0),
			   (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
			   (0,0,0,0,0,0,0,0,0,0,2,2,2,2,0,0,0,0,0,0,0,0),
			   (0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0),
			   (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
			   (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1),
			   (0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1),
			   (0,0,0,0,0,0,0,0,0,0,0,0,5,0,0,0,5,0,0,0,5,1),
			   (0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,0,0,0,5,0,0,1),
			   (0,0,0,0,0,0,0,0,0,0,0,0,5,0,0,0,5,0,0,0,5,1))

	walls18 = ((0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0),
			   (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0),
			   (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0),
			   (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0),
			   (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
			   (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
			   (0,0,0,0,0,0,0,0,1,1,0,0,0,1,1,0,0,0,0,0,0,0),
			   (0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
			   (0,0,0,0,0,0,6,0,0,0,0,6,0,0,0,0,6,0,0,0,0,0),
			   (0,0,0,0,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3))

	walls19 = ((0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,1),
			   (0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1),
			   (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,1),
			   (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1),
			   (0,0,0,0,2,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,1),
			   (0,0,1,0,2,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,1),
			   (0,0,0,0,2,2,2,2,2,0,0,0,0,0,0,0,0,1,1,0,0,1),
			   (0,0,0,0,6,0,6,0,6,0,0,0,0,0,0,0,1,0,0,1,0,1),
			   (0,0,0,0,3,3,3,3,3,0,0,0,0,0,0,1,0,0,0,0,1,1),
			   (0,0,0,0,3,3,3,3,3,0,0,0,0,0,1,0,0,0,0,0,0,1))

	walls110 = ((0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
			    (0,0,0,0,0,0,0,0,0,0,0,0,2,2,0,0,0,0,0,0,0,0),
			    (0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0),
			    (0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,4,0,0,0,0,0,4),
			    (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
			    (1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0),
			    (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0),
			    (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,0,0),
			    (0,0,0,0,0,0,0,0,0,0,0,0,5,0,0,0,5,0,1,2,0,0),
			    (0,0,0,0,0,0,2,2,2,0,0,0,0,0,5,0,0,0,1,2,0,0))

	tip1 = 'Use the arrow keys to move around! Press UP to jump!'
	tip2 = 'Avoid bugs and other animals! They will make you lose money!'
	tip3 = 'Move underneath a low block and jump up to climb onto it!'
	tip4 = 'Move underneath the blocks and jump up!'
	tip5 = 'Water won\'t make you lose money but you can\'t swim!'
	tip6 = 'Try standing farther away from the wall you want to jump onto.'
	tip7 = 'Why are so many animals fleeing the city???'
	tip8 = 'A dangerous river to cross! Time your jumps.'
	tip9 = 'Should you risk grabbing the coins?'
	tip10 = 'Almost to the end!'

	stageset = {1:[stage11, walls11, tip1], 2:[stage12,walls12, tip2], 3:[stage13,walls13, tip3], 4:[stage14,walls14,tip4], 5:[stage15,walls15,tip5], 6:[stage16,walls16,tip6], 7:[stage17,walls17,tip7], 8:[stage18,walls18,tip8], 9:[stage19,walls19,tip9], 10:[stage110,walls110,tip10]}
	currentstage = 1
	stage = stageset[currentstage][0]
	walls = stageset[currentstage][1]
	tip = stageset[currentstage][2]

	blocksize = (Width / 8, Height / 4)
	blocks = {0:images['dirt'], 1:images['grass'], 3:images['water']}
	x = 0
	y = 230

	bg = pygame.Surface((Width, Height))
	bg.convert()

	stagemanager(x, y, bg, Width, Height, stage, blocksize, blocks)

# Load mountains.
# This could be made a function to allow different backdrops for
# different levels. A country level, a city level, etc.
	mountimage = pygame.image.load(path.join(scriptpath, 'assets', 'mountain.png')).convert_alpha()
	mountimage = pygame.transform.scale(mountimage,(100,100))
	mountSurface = pygame.Surface((Width * 2, mountimage.get_height()))
	mCount = Width / mountimage.get_width()
	mCount += 10
	for count in xrange(mCount):
		mountSurface.blit(mountimage, (x,0))
		x += mountimage.get_width()
	x = 0

	mountSurface.set_colorkey(color['black'])

	score = 0

	player = PlayerSprite(scriptpath, (5, 250), Width)
	cloud1 = CloudSprite(scriptpath, (10, 10))
	cloud2 = CloudSprite(scriptpath, (400, 40))
	mountains = MountainLayer(mountSurface, Width, (-400,130))


	scoretext = ScoreField(score, font, tip)

	walllist, traplist, moneylist, enemylist = obstaclemanager(walls, scriptpath)

	enemygroup = pygame.sprite.Group(enemylist)
	moneygroup = pygame.sprite.Group(moneylist)
	wallgroup = pygame.sprite.Group(walllist)
	trapgroup = pygame.sprite.Group(traplist)
	allsprites = pygame.sprite.LayeredDirty(cloud1, cloud2, mountains, player, walllist, moneylist, enemylist, scoretext)



	debug = False #True
	paused = False
	running = True
	done = False
	while True:
		clock.tick(30)
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				exit()
			if event.type == KEYDOWN:
				if event.key == K_p:
					if running:
						if paused:
							paused = False
						else:
							paused = True
				if event.key == K_LEFT:
					if not player.r:
						player.l = True
						if player.rect.x > 100:
							mountains.r = True
						else:
							mountains.l, mountains.r = False, False
				elif event.key == K_RIGHT:
					if not player.l:
						player.r = True
						if player.rect.x < 700:
							mountains.l = True
						else:
							mountains.l, mountains.r = False, False
			if event.type == KEYUP:
				if event.key == K_ESCAPE:
					pygame.quit()
					exit()
				if event.key == K_LEFT:
					if player.l:
						player.l = False
						mountains.r, mountains.l = False, False
				elif event.key == K_RIGHT:
					if player.r:
						player.r = False
						mountains.l, mountains.r = False, False
				if event.key == K_UP:
					if not player.jstep1 and not player.jstep2:
						jump.play()
						player.newy = player.rect.y
						player.jstep1 = True

		while paused:
			pygame.mixer.pause()
			pygame.mixer.music.pause()
			if pygame.event.wait().type == KEYDOWN:
				if pygame.event.wait().key == K_p:
					paused = False
					player.l, player.r = False, False
					pygame.mixer.unpause()
					pygame.mixer.music.unpause()

		if running:
			allsprites.clear(screen, bg)
			allsprites.update()

			if player.rect.right >= Width:
				if currentstage == len(stageset):
					running = False
				else:
					print 'load next street!'
					player.rect.x = 5
					currentstage += 1
					stage = stageset[currentstage][0]
					walls = stageset[currentstage][1]
					tip = stageset[currentstage][2]
					stagemanager(x, y, bg, Width, Height, stage, blocksize, blocks)
					walllist, traplist, moneylist, enemylist = obstaclemanager(walls, scriptpath)
					allsprites.remove(wallgroup, trapgroup, moneygroup, enemygroup, scoretext)
					wallgroup.clear(screen, bg)
					trapgroup.clear(screen,bg)
					moneygroup.clear(screen, bg)
					enemygroup.clear(screen, bg)
					#scoretext.clear(screen, bg)
					wallgroup = pygame.sprite.Group(walllist)
					trapgroup = pygame.sprite.Group(traplist)
					moneygroup = pygame.sprite.Group(moneylist)
					enemygroup = pygame.sprite.Group(enemylist)
					scoretext = ScoreField(score, font, tip)
					allsprites.add(walllist, moneylist, enemylist, scoretext)
					screen.blit(bg, (0,0))
#					tiptext = font.render(tip, True, color['black'])
#					screen.blit(tiptext, (10, 780))
					pygame.display.update()

			for hit in pygame.sprite.spritecollide(player, wallgroup, False):
				if player.rect.bottom - 15 <= hit.rect.top:
					#print 'wall is beneath player!'
					player.jstep2 = False
					player.topofwall = True
				else:
					if hit.rect.left > player.rect.left:
						print 'wall is right of player'
					if hit.rect.x < player.rect.x:
						print 'wall is left of player'
					if player.l:
						player.rect.x += 15
					if player.r:
						player.rect.x -= 15
					if player.l:
						player.l = False
					if player.r:
						player.r = False
					mountains.l, mountains.r = False, False

			if player.rect.y != player.y:
				if not pygame.sprite.spritecollideany(player, wallgroup):
					if player.topofwall:
						player.jstep2 = True
						player.topofwall = False

			for hit in pygame.sprite.spritecollide(player, trapgroup, False):
				splash.play()
				player.l, player.r, = False, False
				player.rect.x = 5

			if not debug:
				if pygame.sprite.spritecollide(player, enemygroup, False):
					for sprite in enemygroup:
						if pygame.sprite.collide_mask(player, sprite):
							player.l, player.r, = False, False
							player.rect.x, player.rect.y = 5, 250
							player.jstep1, player.jstep2 = False, False
							if score > 0: score -= 1
							scoretext.score = score


			for hitcoin in pygame.sprite.spritecollide(player, moneygroup, True):
				money.play()
				score += 1
				scoretext.score = score

			pygame.display.update(allsprites.draw(screen))

		if not running and not done:
			print 'display score here: ', score
			if score < 0:
				score = 0
			try:
				myfile = open(scorefile, 'rb')
				highscores = load(myfile)
				myfile.close()
				oldhs = highscores[1]
				print oldhs
				oldhs = int(oldhs)
				print oldhs
				oldinit = highscores[0]
				print oldinit
				if score > oldhs:
					newhigh = True
				else:
					newhigh = False
			except IOError:
				newhigh = True

			screen.fill(color['lightblue'])
			end = font.render('Your score is %s' % score, True, \
			color['black'])
			end2 = font.render('Will Meenu succeed in getting to the Apple Store?', True, \
			color['black'])
			end3 = font.render('Will she save enough money to afford a new iPhone???', True, \
			color['black'])
			end4 = font.render('Find out later, as her story will be continued!', True, \
			color['black'])
			textrect = centertext(end2, screen)

			screen.blit(end, (textrect.x,textrect.y-30))
			screen.blit(end2, (textrect.x, textrect.y))
			screen.blit(end3, (textrect.x, textrect.y+30))
			screen.blit(end4, (textrect.x, textrect.y+60))
			pygame.display.update()
			pygame.time.wait(8000)

			if newhigh:
				screen.fill(color['lightblue'])
				askinitials = font.render('Enter your first initial...'\
				, True, color['black'])
				screen.blit(askinitials, (textrect.x,textrect.y))
				pygame.display.update()
				while True:
					e = pygame.event.wait()
					if e.type == KEYDOWN and e.key <= 127:
						try:
							playerinitial = chr(e.key)
							playerinitial = playerinitial.upper()
							if playerinitial in ['A','B','C','D','E',\
'F', 'G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V',\
'W','X','Y','Z']:

								oldinit = playerinitial
								oldhs = score
								highscores = [playerinitial, str(score)]
								myfile = open(scorefile, 'wb')
								dump(highscores, myfile)
								myfile.close()
								break
						except:
							pass
			else:
				pygame.display.update()
				pygame.time.wait(1000)

			screen.fill(color['lightblue'])
			credits1 = font.render('Game: Mandeep Shergill', True, \
			color['black'])

			credits2 = font.render\
('Music: Kevin MacLeod', True, color['black'])
			credits3 = font.render\
('"PlanetCute" art by Daniel Cook (Lostgarden.com)', True, color['black'])

			highestscore = font.render('Highest score: %s %s' % \
			(oldinit, oldhs), True, color['black'])

			exitmess = font.render('Press the Esc key to quit', True, \
			color['black'])

			textrect = centertext(credits1, screen)
			screen.blit(highestscore, (textrect.x,textrect.y))
			screen.blit(credits1, (textrect.x,textrect.y+30))
			screen.blit(credits2, (textrect.x,textrect.y+60))
			screen.blit(credits3, (textrect.x-100,textrect.y+90))
			screen.blit(exitmess, (textrect.x,textrect.y+120))
			pygame.display.update()
			done = True

if __name__ == '__main__':
	#import psyco
#	import cProfile as profile
#	psyco.full()
#	profile.run('main()')
	main()
