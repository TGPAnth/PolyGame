# -*- coding: utf-8 -*-

import pygame, sys, copy,math,time
from mmap import *
from poly import *
from pygame.locals import *
pygame.init()

MLOG = 0

MAX_ANGLE_DELTA   = 10

WD = 640
HG = 480

fpsClock = pygame.time.Clock()

windowSurfaceObj = pygame.display.set_mode((WD,HG))
pygame.display.set_caption('Display caption')

redcolor = pygame.Color(255,0,0)
greencolor = pygame.Color(0,255,0)
bluecolor = pygame.Color(0,0,255)
whitecolor = pygame.Color(255,255,255)
SensorRadius = 20

mousex,mousey = 0,0

GameMap = Map(WD,HG)

GameMap.add(Polygon([[1,1],[18,1],[18,14],[1,14]]),WALL)
GameMap.add(Polygon([[2,2],[5,2],[5,5],[2,5]]),WALL)
GameMap.add(Polygon([[11,5],[11,2],[17,2],[17,5]]),WALL)
GameMap.add(Polygon([[2,6],[3,6],[3,12],[2,12]]),WALL)
GameMap.add(Polygon([[11,6],[15,6],[15,8],[11,8]]),WALL)
GameMap.add(Polygon([[15,9],[17,9],[17,13],[15,13]]),WALL)
GameMap.add(Polygon([[6,3],[10,3],[10,5],[6,5]]),MOVE)
GameMap.add(Polygon([[10,11],[14,11],[14,13],[10,13]]),FINISH)

# FirstWallPoly = Polygon([[6,2],[10,2],[10,7],[6,7]])
# FirstWallPoly.can_move(True)
# GameMap.add(FirstWallPoly)
# GameMap.add(Polygon([[10,7],[16,7],[16,9],[10,9]]))

# GameMap.not_log()

font = pygame.font.Font(None, 36)
pnt = pgn = None
mousexy = pygame.mouse.get_pos()

def mouse_button_up(mGameMap):
	if not(mGameMap.ActivePolygonNum == None):
		mGameMap.polygons_array[mGameMap.ActivePolygonNum] = copy.deepcopy(mGameMap.ActivePolygon)
	mGameMap.Mode = CHOOSE
	if not(mGameMap.ActivePolygon==None) and not(mGameMap.ActivePolygonNum==None): 
		mGameMap.polygons_array[mGameMap.ActivePolygonNum] = copy.deepcopy(mGameMap.ActivePolygon)
	mGameMap.ActivePolygon = None
	mGameMap.NewActivePolygon = None
	mGameMap.FreezedPoint = None
	mGameMap.ActivePoint = None
	mGameMap.ActivePolygonNum = None
	mGameMap.StartAngle = None
	mGameMap.AngleNow = None
	mGameMap.ActivePointNum = None
	mGameMap.delta_prev = None

def have_a_winner():
	f = lambda x:[[int(y[0]),int(y[1])] for y in x]
	ready = 0
	for i in GameMap.polygons_array[:]:
		# for x in GameMap.finish_array[:]:
		# 	print f(x)
		if [x for x in GameMap.finish_array[:] if f(x[:])==f(i[:])]:
			ready+=1
	if ready == len(GameMap.finish_array):
		return True
	return False

def print_mouse(mouse_pos):
	strng = "mouse: " + str([mouse_pos[0]/float(GameMap.Scale),mouse_pos[1]/float(GameMap.Scale)])
	text = font.render(strng, 1, (10, 10, 10))
	textpos = text.get_rect()
	textpos.centerx = windowSurfaceObj.get_rect().centerx
	windowSurfaceObj.blit(text, textpos)

def get_pos_angle(angle):
	if angle<0:
		return angle+360
	return angle

while 1:
	# draw background and coordinate grid
	windowSurfaceObj.fill(whitecolor)
	windowSurfaceObj.blit(GameMap.redraw(),(0,0))
	
	# можем ли двигать текущий полигон
	if GameMap.Mode == MOVE :
		if not(GameMap.move_polygons(mousexy,MAX_ANGLE_DELTA)):
			mouse_button_up(GameMap)
			# print 'UP'
	else:
		if have_a_winner():
			mouse_button_up(GameMap)
			windowSurfaceObj.fill(whitecolor)
			windowSurfaceObj.blit(GameMap.redraw(),(0,0))
			pygame.display.update()
			# time.sleep(1)
			strng = "You are WINNER!"
			text = font.render(strng, 1, (10, 10, 10))
			textpos = text.get_rect()
			textpos.centerx = windowSurfaceObj.get_rect().centerx
			windowSurfaceObj.blit(text, textpos)
			raise Exception('You are win')

 
	if MLOG: 
		print_mouse(mousexy)	
	
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

		elif event.type == MOUSEBUTTONDOWN:
			# mouse_button_up()
			mousexy = pygame.mouse.get_pos()
			# 1 - LB 2 - MB 3 - RB 4 - SU 5 - SD
			if (event.button == 1) and (GameMap.Mode == CHOOSE):
				GameMap.Mode = MOVE
				GameMap.mouse_near_corner(mousexy,r=SensorRadius)
				if (GameMap.ActivePolygon==None) or (GameMap.ActivePoint == None):
					GameMap.Mode = CHOOSE
					GameMap.ActivePolygon, GameMap.ActivePoint = None, None
				else:
					GameMap.get_oppose_corner(GameMap.ActivePolygon,GameMap.ActivePoint)
					GameMap.get_index(GameMap.ActivePolygon)
					# print ActivePolygonNum
					GameMap.get_start_angle(GameMap.ActivePolygon,GameMap.ActivePoint)
					GameMap.AngleNow = copy.deepcopy(GameMap.StartAngle)
					GameMap.NewActivePolygon = copy.deepcopy(GameMap.ActivePolygon)
			
		elif event.type == MOUSEMOTION:
			mousexy = pygame.mouse.get_pos()

		elif event.type == MOUSEBUTTONUP:
			mousexy = pygame.mouse.get_pos()
			if event.button == 1:
				mouse_button_up(GameMap)

		elif event.type == KEYDOWN:
			if event.key == K_SPACE:
				for i in GameMap.polygons_array:
					print i
				for i in GameMap.finish_array:
					print i

		elif event.type == KEYUP:
			if event.key == K_SPACE:
				pass

	pygame.display.update()
	fpsClock.tick(30)