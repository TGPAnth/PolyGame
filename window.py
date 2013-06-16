# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
#pygame.init()
class Window(object):

	def __init__(self,wd=640,hg=480,caption=''):
		self.redcolor = pygame.Color(255,0,0)
		self.greencolor = pygame.Color(0,255,0)
		self.bluecolor = pygame.Color(0,0,255)
		self.whitecolor = pygame.Color(255,255,255)
		self.windowSurfaceObj = pygame.display.set_mode((wd,hg))
		pygame.display.set_caption(caption)
		#return self.windowSurfaceObj

	def update(self,GM):
		# draw background and coordinate grid
		self.windowSurfaceObj.fill(self.whitecolor)
		self.windowSurfaceObj.blit(GM.redraw(),(0,0))