# -*- coding: utf-8 -*-
import pygame, sys, copy,math,time
from pprint import pprint
from mmap import *
from window import Window
from poly import *
from level import Level
from pygame.locals import *
pygame.init()

MLOG = 0

class Game(object):

	def __init__(self):
		self.MAX_ANGLE_DELTA   = 10
		self.WD = 640
		self.HG = 480
		self.lvl_now = 0
		self.fpsClock = pygame.time.Clock()
		self.SensorRadius = 20
		self.mousex,self.mousey = 0,0
		self.GameMap = Map(self.WD,self.HG)
		self.MainWindow = Window()
		self.Levels = Level()
		self.now_lvl()
		self.font = pygame.font.Font(None, 36)
		self.pnt = self.pgn = None
		self.mousexy = pygame.mouse.get_pos()
		self.fpsClock = pygame.time.Clock()
		
	def now_lvl(self):
		self.GameMap.load_level(self.Levels[self.lvl_now])

	def mouse_button_up(self,GameMap):
		if not(self.GameMap.ActivePolygonNum == None):
			self.GameMap.polygons_array[self.GameMap.ActivePolygonNum] = copy.deepcopy(self.GameMap.ActivePolygon)
		self.GameMap.Mode = CHOOSE
		if not(self.GameMap.ActivePolygon==None) and not(self.GameMap.ActivePolygonNum==None): 
			self.GameMap.polygons_array[self.GameMap.ActivePolygonNum] = copy.deepcopy(self.GameMap.ActivePolygon)
		self.GameMap.ActivePolygon = None
		self.GameMap.NewActivePolygon = None
		self.GameMap.FreezedPoint = None
		self.GameMap.ActivePoint = None
		self.GameMap.ActivePolygonNum = None
		self.GameMap.StartAngle = None
		self.GameMap.AngleNow = None
		self.GameMap.ActivePointNum = None
		self.GameMap.delta_prev = None

	def have_a_winner(self):
		f = lambda x:[[int(y[0]),int(y[1])] for y in x]
		ready = 0
		for i in self.GameMap.polygons_array[:]:
			if [x for x in self.GameMap.finish_array[:] if f(x[:])==f(i[:])]:
				ready+=1
		if ready == len(self.GameMap.finish_array):
			return True
		return False

	def get_pos_angle(self,angle):
		if angle<0:
			return angle+360
		return angle

	def next_level(self):
		self.lvl_now += 1
		self.GameMap.load_level(Levels[self.lvl_now])

	def main_loop(self):
		while 1:			
			# можем ли двигать текущий полигон
			if self.GameMap.Mode == MOVE :
				if not(self.GameMap.move_polygons(self.mousexy,self.MAX_ANGLE_DELTA)):
					self.mouse_button_up(self.GameMap)
					# print 'UP'
			else:
				if self.have_a_winner():
					self.mouse_button_up(self.GameMap)
					self.MainWindow.update(self.GameMap)
					pygame.display.update()
					strng = "You are WINNER!"
					text = font.render(strng, 1, (10, 10, 10))
					textpos = text.get_rect()
					textpos.centerx = self.MainWindow.windowSurfaceObj.get_rect().centerx
					self.MainWindow.windowSurfaceObj.blit(text, textpos)
					#raise Exception('You are win')
		 
			if MLOG: 
				self.print_mouse(self.mousexy)	
			
			self.user_action()

			pygame.display.update()
			self.fpsClock.tick(30)

	def user_action(self):
		for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()

				elif event.type == MOUSEBUTTONDOWN:
					# mouse_button_up()
					self.mousexy = pygame.mouse.get_pos()
					# 1 - LB 2 - MB 3 - RB 4 - SU 5 - SD
					if (event.button == 1) and (self.GameMap.Mode == CHOOSE):
						self.start_move()
					
				elif event.type == MOUSEMOTION:
					self.mousexy = pygame.mouse.get_pos()

				elif event.type == MOUSEBUTTONUP:
					self.mousexy = pygame.mouse.get_pos()
					if event.button == 1:
						self.mouse_button_up()

				elif event.type == KEYDOWN:
					if event.key == K_SPACE:
						for i in self.GameMap.polygons_array:
							print i
						for i in self.GameMap.finish_array:
							print i

				elif event.type == KEYUP:
					if event.key == K_SPACE:
						pass

	def start_move(self):
		self.GameMap.Mode = MOVE
		self.GameMap.mouse_near_corner(self.mousexy,r=self.SensorRadius)
		if (self.GameMap.ActivePolygon==None) or (self.GameMap.ActivePoint == None):
			self.GameMap.Mode = CHOOSE
			self.GameMap.ActivePolygon, self.GameMap.ActivePoint = None, None
		else:
			self.GameMap.get_oppose_corner(self.GameMap.ActivePolygon,self.GameMap.ActivePoint)
			self.GameMap.get_index(self.GameMap.ActivePolygon)
			self.GameMap.get_start_angle(self.GameMap.ActivePolygon,self.GameMap.ActivePoint)
			self.GameMap.AngleNow = copy.deepcopy(self.GameMap.StartAngle)
			self.GameMap.NewActivePolygon = copy.deepcopy(self.GameMap.ActivePolygon)

	def start_game(self):
		pass

	def menu_screen(self):
		pass

	def flash_screen(self):
		pass

	def level_screen(self):
		pass

	def options_screen(self):
		pass

	def game_screen(self):
		pass

if __name__=="__main__":
	mainGame = Game()
	mainGame.main_loop()
