#!/usr/bin/env python2.6
# A Breakout-style game
# First of my games to use tiling

# At start you can use vector aim to shoot at any point, ball bounces
# off walls and player, breaks phones. If it hits floor it breaks,
# 3 ball limit

from cPickle import dump, load
from sys import exit
from os import path, environ
from math import sin, cos, pi
from random import randint #, choice
import pygame
from pygame.locals import *
from pygame.color import THECOLORS as color

# 3 different object types: Player, ball, phone. Two subclasses of phone

class iPhoneSprite(pygame.sprite.DirtySprite):
	image = None
	def __init__(self, scriptpath, pos):
		self.dirty = 0
		pygame.sprite.DirtySprite.__init__(self)
		if iPhoneSprite.image == None:
			iPhoneSprite.image = pygame.image.load(path.join\
			(scriptpath, 'assets', 'iphone1.png')).convert_alpha()
#		self.id = i
		self.rect = pygame.Rect(pos[0], pos[1], self.image.get_width(),\
		self.image.get_height())


class AndroidSprite(iPhoneSprite):
	image = None
	def __init__(self, scriptpath, pos):
		self.dirty = 0
		pygame.sprite.DirtySprite.__init__(self)
		if AndroidSprite.image == None:
			AndroidSprite.image = pygame.image.load(path.join\
			(scriptpath, 'assets', 'nexus1.png')).convert_alpha()
#		self.id = i
		self.rect = pygame.Rect(pos[0], pos[1], self.image.get_width(),\
		self.image.get_height())


class PaddleSprite(pygame.sprite.DirtySprite):
	def __init__(self):
		self.dirty = 1
		pygame.sprite.DirtySprite.__init__(self)
		self.image = pygame.Surface((150,12))#100,12))
#		pygame.draw.line(self.image, color['green'], (0,0), (150,0))
		self.rect = pygame.Rect(565, 788, 150, 12)
		self.image.fill(color['red'])
		self.start = pygame.Rect(565, 788, 150, 12)
		self.left, self.right = False, False
		self.speed = 25 #30

	def update(self):
		self.dirty = 1
		if self.left and  self.rect.left > 0:
			self.rect.left -= self.speed
		if self.right and self.rect.right < 1280:
			self.rect.left += self.speed


class BallSprite(pygame.sprite.DirtySprite):
	def __init__(self, paddle):
		self.dirty = 1
		pygame.sprite.DirtySprite.__init__(self)
		self.image = pygame.Surface((10,10))
		self.image.fill(color['green'])
		pygame.draw.circle(self.image, color['orange'], \
		self.image.get_rect().center, 5)
		self.image.set_colorkey(color['green'])
		self.rect = pygame.Rect(640, 778, 10,10)
		self.start = pygame.Rect(640, 778, 10,10)
		self.firstmove = False
		self.moving = False
		self.lor, self.uod = None, None
		self.speed = 10 #20
		self.up, self.down, self.left, self.right = 1, 2, 3, 4
		self.angle = 0
		self.dx, self.dy = 0, 0
		self.paddle = paddle

	def randangle(self):
		self.angle = randint(1,360) * (pi / 180) #choice((10,20,30,40,50,60,70,80,90))#
		self.dx = self.speed * cos(self.angle)
		self.dy = self.speed * sin(self.angle)
		self.dy *= -1

		if self.dy > -10: self.dy = -10 #*= -1
		#if not self.dy: self.dy = -30

	def update(self):
		self.dirty = 1
		if self.firstmove and not self.moving:
#			self.lor = self.left
			self.randangle()
			if self.paddle.right and self.dx < 1:
				self.dx *= -1
			elif self.paddle.left and self.dx > 1:
				self.dx *= -1
#			self.uod = self.up
			self.firstmove = False
			self.moving = True

#		if not self.angle:
#			if self.lor == self.left:
#				self.rect.left -= self.speed
#			if self.lor == self.right:
#				self.rect.left += self.speed

		if self.angle:
			self.rect.x += self.dx
			self.rect.y += self.dy

#		if self.uod == self.down:
#			self.dy *= -1
#			self.rect.top += self.speed
#		if self.uod == self.up:
#			self.rect.top -= self.speed

		if self.rect.top <= 0:
#			self.uod = self.down
			self.dy = -1 * self.dy
		if self.rect.left <= 0:
#			self.lor = self.right
			self.dx = -1 * self.dx
		if self.rect.right >= 1280:
#			self.lor = self.left
			self.dx = -1 * self.dx


def centertext(text, screen):
	textrect = text.get_rect()
	textrect.centerx = screen.get_rect().centerx
	textrect.centery = screen.get_rect().centery
	return textrect

def main():
	pygame.mixer.pre_init(22050, -16, 2, 512)
	pygame.init()
	environ['SDL_VIDEO_CENTERED'] = '1'
	pygame.display.set_caption('iBreakout')
	Width = 1280
	Height = 800
	scriptpath = path.dirname(__file__)
	screen = pygame.display.set_mode((Width, Height),FULLSCREEN)
	pygame.mouse.set_visible(0)
	font = pygame.font.Font(None, 32)
	linespace = pygame.font.Font.get_linesize(font)
	clock = pygame.time.Clock()
	scorefile = path.join(scriptpath, 'assets', 'scores.data')
	explosion = pygame.mixer.Sound(path.join(scriptpath, 'assets', 'explosion.ogg'))
	oops = pygame.mixer.Sound(path.join(scriptpath, 'assets', 'oops.ogg'))
	pygame.mixer.music.load(path.join(scriptpath, 'assets', 'music.ogg'))
	pygame.mixer.music.play(-1, 0.0)

	intro = font.render("Let's Play Breakout!", True, \
	color['white'])
	textrect = centertext(intro, screen)
	screen.fill(color['black'])
	screen.blit(intro, textrect)
	pygame.display.update()
	pygame.time.wait(1000)

	phones = [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
			  [1,1,1,1,2,2,1,1,1,1,1,0,0,1,1,1,0,0,1,1,1,1,1,2,2,1,1,1,1],
			  [1,1,1,1,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,1,1,1,1],
			  [1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1],
			  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
#			  [1,1,1,0,0,0,0,1,1,1,1,1,1,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1],
#			  [1,1,1,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
#			  [1,1,1,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
			  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]

	phonelist = []

#	iphonecount = 0
	iphonelocations = []
#	androidcount = 0
	androidlocations = []
#	x = 250; y = 100
	x = 17; y = 1
	phoneWidth =  43
	phoneHeight = 79

	mapobjects = (iphonelocations, androidlocations)
	for row in phones:
		for thing in row:
# if thing is 1, instantiate iphonesprite at loc, add to list
			if thing:
				mapobjects[thing - 1].append((x,y))

#			if thing:
#				iphonecount += 1
#				iphonelocations.append((x,y))
#			else:
#				androidcount += 1
#				androidlocations.append((x,y))
			x += phoneWidth #40
		y += phoneHeight #40
		x = 17 #250

	iphones = []
	droids = []
#	for i in range(1, iphonecount+1):
	for pos in iphonelocations:
		iphones.append(iPhoneSprite(scriptpath, pos))

	phonelist.append(iphones)

#	for i in range(1, androidcount+1):
	for pos in androidlocations:
		droids.append(AndroidSprite(scriptpath, pos))

	phonelist.append(droids)

	paddle = PaddleSprite()
	ball = BallSprite(paddle)
	bg = pygame.image.load(path.join(scriptpath, 'assets', 'image.png'\
	)).convert()

# Intro/title screen
	intro = font.render('Break all the iPhones, but avoid the Android /n phones!', True, \
	color['white'])

#	textrect = centertext(intro, screen)
# While testing comment out the following:
#	screen.fill(color['black'])
#	screen.blit(intro, textrect)
#	pygame.display.update()
#	pygame.time.wait(1750)


	bg = pygame.transform.scale(bg, (Width, Height))
	screen.blit(bg, (0,0))
	phonegroup = pygame.sprite.LayeredDirty(phonelist)
	paddlegroup = pygame.sprite.LayeredDirty(paddle)
	allsprites = pygame.sprite.LayeredDirty(phonelist, ball, paddle)

	score = 0
	ballcount = 3
	paused = False
	running = True
	done = False
	pygame.event.set_blocked(MOUSEMOTION)
	takinginput = True
	while True:
		clock.tick(30)
#		pygame.time.wait(10)
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
				if running and takinginput:
					if event.key == K_LEFT:
						if not ball.firstmove and not ball.moving:
							ball.firstmove = True
#							if ball.dx > 1:
#								ball.dx *= -1
						paddle.right = False
						paddle.left = True
					if event.key == K_RIGHT:
						if not ball.firstmove and not ball.moving:
							ball.firstmove = True
#							if ball.dx < 1:
#								ball.dx *= -1
						paddle.right = True
						paddle.left = False
			if event.type == KEYUP:
				if event.key == K_ESCAPE:
					pygame.quit()
					exit()
				if event.key == K_LEFT:
					paddle.left = False
				if event.key == K_RIGHT:
					paddle.right = False

		while paused:
			pygame.mixer.pause()
			pygame.mixer.music.pause()
			if pygame.event.wait().type == KEYDOWN:
				if pygame.event.wait().key == K_p:
					paused = False
					pygame.mixer.unpause()
					pygame.mixer.music.unpause()

# At start ball moves at a specified angle, direction determined by
# what direction arrow key is pressed. Ball bounces off phones and walls
# at this angle. Angle changes when ball hits paddle again, new angle
# depends on part of paddle hit. As ball hits phone instance, the phone
# is deleted and score raised.

		if running:
			allsprites.clear(screen, bg)
			allsprites.update()

			if pygame.sprite.spritecollide(ball, paddlegroup, \
			False):

				ball.randangle()
				if paddle.right and ball.dx < 1:
					ball.dx *= -1
				elif paddle.left and ball.dx > 1:
					ball.dx *= -1

			if pygame.sprite.spritecollide(ball, phonegroup, \
			True):
				explosion.play()
				score += 100
				ball.randangle()
				ball.dy *= -1
				#ball.dx *= -1


			if ball.rect.top >= Height:
				oops.play()
				takinginput = False
				ball.rect.x, ball.rect.y = ball.start.x, ball.start.y
				paddle.rect.x, paddle.rect.y = paddle.start.x, paddle.\
				start.y
				ball.angle = 0
				ball.firstmove = False
				ball.moving = False
				ballcount -= 1
				print 'ball lost, # left is ', ballcount
				score -= 100
				pygame.time.wait(1000)
				takinginput = True

			pygame.display.update(allsprites.draw(screen))

			if ballcount <= 0 or len(phonegroup) < 1:
#				print 'game over'
				running = False
#				break

# Score screen, add replay option
		if not running and not done:
			pygame.mouse.set_visible(0)

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

			screen.fill(color['black'])
			end = font.render('Your score is %s' % score, True, \
			color['white'])

			centertext(end, screen)

			screen.blit(end, (textrect.x,textrect.y-30))
			if newhigh:
				askinitials = font.render('Enter your first initial...'\
				, True, color['white'])

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
				pygame.time.wait(2000)

			screen.fill(color['black'])
			credits1 = font.render('Game: Mandeep Shergill', True, \
			color['white'])

			credits2 = font.render\
('Music: Kevin MacLeod', True, color['white'])

			highestscore = font.render('Highest score: %s %s' % \
			(oldinit, oldhs), True, color['white'])

			exitmess = font.render('Press the Esc key to quit', True, \
			color['white'])

			textrect = centertext(credits1, screen)
			screen.blit(highestscore, (textrect.x,textrect.y+30))
			screen.blit(credits1, (textrect.x,textrect.y+60))
			screen.blit(credits2, (textrect.x,textrect.y+90))
			screen.blit(exitmess, (textrect.x,textrect.y+120))
			pygame.display.update()
			done = True

if __name__ == '__main__':
#	import psyco
#	psyco.full()
	main()
#	import pstats
#	import cProfile as profile
#	profile.run('main()', "Profile.prof")
#	s = pstats.Stats("Profile.prof")
#	s.strip_dirs().sort_stats("time").print_stats(10)
