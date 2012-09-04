# -*- coding: utf-8 -*-

import pygame, sys, copy,math
from mmap import *
from poly import *
from pygame.locals import *
pygame.init()

CanLog = 0

# sys.getsizeof

MLOG = 0

MAX_ANGLE_DELTA_K = 0.11111
MAX_ANGLE_DELTA   = 10

WD = 640
HG = 480

# while True:
# 	get_active_poly
# 	get_rotate_point
# 	get_angle
# 	get_results

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

FirstWallPoly = Polygon([[6,2],[10,2],[10,7],[6,7]])
FirstWallPoly.can_move(True)
GameMap.add(FirstWallPoly)
GameMap.add(Polygon([[10,7],[16,7],[16,9],[10,9]]))

GameMap.not_log()

font = pygame.font.Font(None, 36)
pnt = pgn = None
mousexy = pygame.mouse.get_pos()

def mouse_button_up():
	global GameMap
	if not(GameMap.ActivePolygonNum == None):
		GameMap.polygons_array[GameMap.ActivePolygonNum] = copy.deepcopy(GameMap.ActivePolygon)
	GameMap.Mode = CHOOSE
	if not(GameMap.ActivePolygon==None) and not(GameMap.ActivePolygonNum==None): 
		GameMap.polygons_array[GameMap.ActivePolygonNum] = copy.deepcopy(GameMap.ActivePolygon)
	GameMap.ActivePolygon = None
	GameMap.NewActivePolygon = None
	GameMap.FreezedPoint = None
	GameMap.ActivePoint = None
	GameMap.ActivePolygonNum = None
	GameMap.StartAngle = None
	GameMap.AngleNow = None
	GameMap.ActivePointNum = None
	GameMap.delta_prev = None

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

def sign(a):
	if a<0:
		return -1
	return 1

while 1:
	# draw background and coordinate grid
	windowSurfaceObj.fill(whitecolor)
	windowSurfaceObj.blit(GameMap.redraw(),(0,0))
	
	# print GameMap.get_AS()

	# можем ли двигать текущий полигон
	if GameMap.Mode == MOVE and not GameMap.move_polygons(mousexy,MAX_ANGLE_DELTA):
		mouse_button_up()
 
	if MLOG: 
		print_mouse(mousexy)	
	
	CanLog = 0
	GameMap.not_log()
	# get events
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
				mouse_button_up()

		elif event.type == KEYDOWN:
			if event.key == K_SPACE:
				if CanLog:
					GameMap.not_log()
				else:
					CanLog = 1
					GameMap.log()

		elif event.type == KEYUP:
			if event.key == K_SPACE:
				GameMap.not_log()
				CanLog = 0

	pygame.display.update()
	fpsClock.tick(30)