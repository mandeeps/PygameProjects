#!/usr/bin/env python2.6
# Grab as much fruit as fast as you can without getting caught
# Score calc = +100 point for each fruit, -10 for each second spent
# +500 for getting all of them

#import psyco
from os import path
from cPickle import dump, load
from sys import exit
from random import choice, randint
from time import time
import pygame
from pygame.locals import *
from pygame.color import THECOLORS as color
#pygame.mixer.pre_init(44100, -16, 2, 512)

def main():
	pygame.init()
	pygame.mouse.set_visible(0)
	pygame.display.set_caption('Juicer')
	Window = pygame.display.set_mode((0,0),FULLSCREEN)#(Width, Height),FULLSCREEN)#|HWSURFACE|DOUBLEBUF)
	Width, Height = Window.get_size()
	Font = pygame.font.Font(None, 32)
	scriptpath = path.dirname(__file__)
	scorefile = path.join(scriptpath, 'Data', 'scores.data')
	icon = pygame.image.load(path.join(scriptpath, 'Data', 'icon.png')).convert_alpha()
	pygame.display.set_icon(icon)
	fruitimage = pygame.image.load(path.join(scriptpath, 'Data','berry.png')).convert_alpha()
	playerimage = pygame.image.load(path.join(scriptpath, 'Data','gobi.png')).convert_alpha()
	sheruimage = pygame.image.load(path.join(scriptpath, 'Data','sheru.png')).convert_alpha()
	sheru2image = pygame.image.load(path.join(scriptpath, 'Data','sheru2.png')).convert_alpha()
	bg = pygame.image.load(path.join(scriptpath, 'Data','grass.jpg')).convert(16)
	dogimage = pygame.image.load(path.join(scriptpath, 'Data','dog.png')).convert_alpha()
	dog2image = pygame.image.load(path.join(scriptpath, 'Data','dog2.png')).convert_alpha()
	bgimage = pygame.transform.scale(bg, (Width, Height))
	pygame.mixer.music.load(path.join(scriptpath, 'Data', 'music.ogg'))
	pygame.mixer.music.play(-1, 0.0)
	deathsound = pygame.mixer.Sound(path.join(scriptpath, 'Data','gameover.ogg'))
	foodgrabsound = pygame.mixer.Sound(path.join(scriptpath, 'Data','pickup.ogg'))
	allfoodgonesound = pygame.mixer.Sound(path.join(scriptpath, 'Data', 'victory.ogg'))

# sprite masks for advanced collision detection
	playermask = pygame.mask.from_surface(playerimage)
	dogmask1 = pygame.mask.from_surface(dogimage)
	dogmask2 = pygame.mask.from_surface(dog2image)
	sherumask1 = pygame.mask.from_surface(sheruimage)
	sherumask2 = pygame.mask.from_surface(sheru2image)

#	facing = ['empty', 'left', 'left', 'left', 'left']

	# directions setup
	up, left, right, down, upleft, downleft, upright, downright = 1, 2, 3, 4, 5, 6, 7, 8
	op = {up:down, left:right, right:left, down:up, upleft:downright, \
downright:upleft, upright:downleft, downleft:upright}
	directions = [up, left, right, down, upleft, downleft, upright, downright]
	speed = 10
	lowspeed = 3
	dogrect = dogimage.get_rect()
	sherurect = sheruimage.get_rect()
	foodcount = 100
	dogcount = 3
	enemylocations = [pygame.Rect(Width - dogrect.width,dogrect.height,dogrect.width,dogrect.height),\
pygame.Rect(dogrect.width,dogrect.height,dogrect.width,dogrect.height), pygame.Rect(Width - dogrect.width, Height - dogrect.height, dogrect.width,dogrect.height)]
	score = 0
	intro = Font.render('Grab the magic moving strawberries and don\'t get caught!', True, color['white'])
	TextRect = intro.get_rect()

	def centertext():
		TextRect.centerx = Window.get_rect().centerx
		TextRect.centery = Window.get_rect().centery

	centertext()
	Window.fill(color['black'])
	Window.blit(intro, TextRect)
	pygame.display.update()
	pygame.time.wait(1750)

	clock = pygame.time.Clock()
	pygame.event.set_blocked(MOUSEMOTION)
	running = True
	done = False

# Base class for Dog, Sheru, Food sprites
	class NonPlayerSprite(pygame.sprite.DirtySprite):
		def __init__(self, image, rect, dir):
			self.dirty = 1
			pygame.sprite.DirtySprite.__init__(self)
			self.image, self.rect, self.dir = (image, rect, dir)

		def update(self):
			self.dirty = 1
			if self.dir == down and self.rect.bottom < Height:
				if self.name == 'sheru':
					self.rect.top += lowspeed
				else: self.rect.top += speed
			elif self.dir == up and self.rect.top > 0:
				if self.name == 'sheru':
					self.rect.top -= lowspeed
				else: self.rect.top -= speed
			elif self.dir == left and self.rect.left > 0:
				if self.name == 'sheru':
					self.rect.left -= lowspeed
				else: self.rect.left -= speed
			elif self.dir == right and self.rect.right < Width:
				if self.name == 'sheru':
					self.rect.left += lowspeed
				else: self.rect.left += speed
			elif self.dir == downleft and self.rect.bottom < Height and self.rect.left > 0:
				if self.name == 'sheru':
					self.rect.top += lowspeed
					self.rect.left -= lowspeed
				else:
					self.rect.top += speed
					self.rect.left -= speed
			elif self.dir == upright and self.rect.top > 0 and self.rect.right < Width:
				if self.name == 'sheru':
					self.rect.top -= lowspeed
					self.rect.left += lowspeed
				else:
					self.rect.top -= speed
					self.rect.left += speed
			elif self.dir == upleft and self.rect.top > 0 and self.rect.left > 0:
				if self.name == 'sheru':
					self.rect.top -= lowspeed
					self.rect.left -= lowspeed
				else:
					self.rect.top -= speed
					self.rect.left -= speed
			elif self.dir == downright and self.rect.bottom < Height and self.rect.right < Width:
				if self.name == 'sheru':
					self.rect.top += lowspeed
					self.rect.left += lowspeed
				else:
					self.rect.top += speed
					self.rect.left += speed
# Wall collision detection
# It is crucial to set this to if-elif instead of if-if because \
# the sprites can and will get stuck when two of them collide near a \
# corner and they are going at an angle that allows their rects to go \
# past two sides of the wall
			if self.rect.top <= 0:
				self.dir = choice([left, right, down, downleft, downright])
			elif self.rect.bottom >= Height:
				self.dir = choice([left, right, up, upleft, upright])
			elif self.rect.left <= 0:
				self.dir = choice([up, down, right, upright, downright])
			elif self.rect.right >= Width:
				self.dir = choice([up, down, left, downleft, upleft])

# Food class inherits from base
	class FoodSprite(NonPlayerSprite):
		def __init__(self, number):
			self.name = 'food'
			self.dirty = True
			pygame.sprite.DirtySprite.__init__(self)
			self.number = number
			self.image, self.rect, self.dir = (fruitimage, pygame.Rect(randint\
(0, Width - 40), randint(0, Height - 27), 40, 27), choice(directions))

# Enemy class
	class EnemySprites(NonPlayerSprite):
		def __init__(self, image, number):
			self.name = 'enemy'
			self.dirty = True
			pygame.sprite.DirtySprite.__init__(self)
			self.number = number
			self.image, self.dir = image, choice(directions)
			self.frame = 0
			if self.image == dogimage:
				self.rect = choice(enemylocations)
				enemylocations.remove(self.rect)
				self.mainimage = dogimage
				self.altimage = dog2image
				self.mask = dogmask1
				self.mask1 = dogmask1
				self.mask2 = dogmask2
			else:
				self.rect = pygame.Rect(sherurect.width,Height-sherurect.height,sherurect.width,sherurect.height)
				self.mainimage = sheruimage
				self.altimage = sheru2image
				self.mask = sherumask1
				self.mask1 = sherumask1
				self.mask2 = sherumask2

		def update(self):
			NonPlayerSprite.update(self)
			self.frame += 1
			if (self.frame / 10) % 2 == 0:
				self.image = self.altimage
				self.mask = self.mask2
			else:
				self.image = self.mainimage
				self.mask = self.mask1

# Custom Sheru subclass to implement chase behavior
	class SheruChaseSprite(EnemySprites):
		def __init__(self, image, number):
			EnemySprites.__init__(self, image, number)
			self.name = 'sheru'
			self.dirty = True
		def update(self):
			EnemySprites.update(self)
			if self.rect.x < player.rect.x and self.rect.y < player.rect.y:
				if self.rect.y+200 >= Height:
					self.dir = right
				else:
					self.dir = downright
			elif self.rect.x > player.rect.x and self.rect.y > player.rect.y:
				self.dir = upleft
			elif self.rect.x < player.rect.x and self.rect.y > player.rect.y:
				self.dir = upright
			elif self.rect.x > player.rect.x and self.rect.y < player.rect.y:
				if self.rect.y+200 >= Height:
					self.dir = left
				else:
					self.dir = downleft
			elif self.rect.x < player.rect.x:
				self.dir = right
			elif self.rect.x > player.rect.x:
				self.dir = left
			elif self.rect.y < player.rect.y:
				self.dir = down
			elif self.rect.y > player.rect.y:
				self.dir = up

# Player class
	class PlayerSprite(pygame.sprite.DirtySprite):
		def __init__(self):
			self.dirty = 1
			pygame.sprite.DirtySprite.__init__(self)
			self.image, self.rect = (playerimage, pygame.Rect(640,400,70,174))
			self.l, self.r, self.u, self.d, self.ul, self.dl, self.ur, self.dr = False, False, False, False, False, False, False, False
			self.mask = playermask

		def update(self):
# character wall detection
			self.dirty = 1
			if self.d and self.rect.bottom < Height:
				self.rect.top += speed
			if self.u and self.rect.top > 0:
				self.rect.top -= speed
			if self.l and self.rect.left > 0:
				self.rect.left -= speed
			if self.r and self.rect.right < Width:
				self.rect.right += speed

	foods = [FoodSprite(i) for i in range(foodcount)]
	dogs = [EnemySprites(dogimage,i) for i in range(dogcount)]
	sheru = SheruChaseSprite(sheruimage,1)#EnemySprites(sheruimage,1)
	player = PlayerSprite()

	foodgroup = pygame.sprite.LayeredDirty(foods)
	enemies = pygame.sprite.LayeredDirty(dogs, sheru)
	allsprites = pygame.sprite.LayeredDirty(foods, dogs, sheru, player)

	paused = False
	starttime = time()
	while True:
		clock.tick(30)
		pygame.time.wait(5)

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				exit()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					pygame.quit()
					exit()
				if event.key == K_p:
					if running:
						if paused:
							paused = False
						else:
							paused = True
				if event.key == K_LEFT:
					player.r = False
					player.l = True
				if event.key == K_RIGHT:
					player.r = True
					player.l = False
				if event.key == K_DOWN:
					player.d = True
					player.u = False
				if event.key == K_UP:
					player.d = False
					player.u = True
			if event.type == KEYUP:
				if event.key == K_LEFT:
					player.l = False
				if event.key == K_RIGHT:
					player.r = False
				if event.key == K_DOWN:
					player.d = False
				if event.key == K_UP:
					player.u = False

		while paused:
			pygame.mixer.pause()
			pygame.mixer.music.pause()
			for event in pygame.event.get():
				if event.type == KEYDOWN:
					if event.key == K_p:
						paused = False
						pygame.mixer.unpause()
						pygame.mixer.music.unpause()

		if running:
			allsprites.clear(Window, bgimage)
#			t = pygame.time.get_ticks()
			allsprites.update()

# When player picks up food, remove food, increase score
#			for hit in pygame.sprite.spritecollide(player, foodgroup, True):
			if pygame.sprite.spritecollide(player, foodgroup, True):
				score += 100
				foodgrabsound.play()

# Player/Enemy collision detection
# Added code for collision mask, pixel-based collision detection
#			for hit in pygame.sprite.spritecollide(player, enemies, False):
#			if pygame.sprite.spritecollide(player, enemies, False):
				for enemy in enemies:
					tempgroup = pygame.sprite.GroupSingle(enemy)
					if pygame.sprite.spritecollide(player, tempgroup, False):
						if pygame.sprite.collide_mask(player, enemy):
							deathsound.play()
							pygame.mixer.music.stop()
							endtext = 'You got hit! Game Over! Score: {0}'
							running = False

# If enemies collide make them change direction
			for foe in enemies:
				EnemiesTemp = pygame.sprite.Group()
				EnemiesTemp.add(enemies)
				EnemiesTemp.remove(foe)
				if pygame.sprite.spritecollide(foe, EnemiesTemp, False):
					fdirchoices = list(directions)
					fdirchoices.remove(foe.dir)
					foe.dir = choice(fdirchoices) #op[foe.dir]

# If all food was picked up
			if len(foodgroup) == 0:
				score +=500
				endtext = 'Good work! Score: {0}'
				allfoodgonesound.play()
				pygame.mixer.music.stop()
				running = False

			pygame.display.update(allsprites.draw(Window))

	# When game is finished, calculate score
		if not running and not done: #running == False and done == False:
			endtime = time()
			starttime = int(starttime)
			endtime = int(endtime)
			totaltime = (endtime - starttime)
			score -= (totaltime * 10)
			if score < 0:
				score = 0
			try:
				myfile = open(scorefile, 'rb')
				highscores = load(myfile)
				myfile.close()
				oldhs = highscores[1]
				oldhs = int(oldhs)
				oldinit = highscores[0]
				if score > oldhs:
					newhigh = True
				else:
					newhigh = False
			except IOError:
				newhigh = True

			Window.fill(color['black'])
			end = Font.render(endtext.format(str(score)), True, color['white'])
			TextRect = end.get_rect()
			centertext()

			Window.blit(end, (TextRect.x,TextRect.y-30))
			if newhigh:
				askinitials = Font.render('Enter your first initial...', True, color['white'])
				Window.blit(askinitials, (TextRect.x,TextRect.y))
				pygame.display.flip()
				while True:
					e = pygame.event.wait()
					if e.type == KEYDOWN and e.key <= 127:
						try:
							playerinitial = chr(e.key)
							playerinitial = playerinitial.upper()
							if playerinitial in ['A','B','C','D','E','F',\
'G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']:
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
				pygame.display.flip()
				pygame.time.wait(2000)

			Window.fill(color['black'])
			credits1 = Font.render('Game: Mandeep Shergill', True, color['white'])
			credits2 = Font.render('Models: Tanvir and Gurvir Shergill. Music: Kevin MacLeod', True, color['white'])
			highestscore = Font.render('Highest score: %s %s' % (oldinit, oldhs), True, color['white'])
			exitmess = Font.render('Press the Esc key to quit', True, color['white'])
			TextRect = credits1.get_rect()
			centertext()
			Window.blit(highestscore, (TextRect.x,TextRect.y+30))
			Window.blit(credits1, (TextRect.x,TextRect.y+60))
			Window.blit(credits2, (TextRect.x-150,TextRect.y+90))
			Window.blit(exitmess, (TextRect.x,TextRect.y+120))
			pygame.display.update()
			done = True

if __name__ == '__main__':
#	psyco.full()
#	import cProfile as profile
#	profile.run('main()')
	main()
