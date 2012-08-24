# -*- coding: utf-8 -*-

import pygame, sys, copy,math
from mmap import *
from poly import *
from pygame.locals import *
pygame.init()

MLOG = 1

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

FirstWallPoly = Polygon([[1,1],[4,1],[4,5],[1,5]])
GameMap.add(FirstWallPoly)
GameMap.add(Polygon([[10,7],[16,7],[16,9],[10,9]]))

ActivePolygonNum = None
ActivePolygon = None
NewActivePolygon = None
FreezedPoint = None
ActivePoint = None
StartAngle = None
AngleNow = None

font = pygame.font.Font(None, 36)
pnt = pgn = None
mousexy = pygame.mouse.get_pos()

def mouse_button_up():
	global ActivePolygon
	global NewActivePolygon
	global FreezedPoint
	global ActivePoint
	global ActivePolygonNum
	global StartAngle
	global AngleNow
	global GameMap

	GameMap.Mode = CHOOSE
	if not(ActivePolygon==None): 
		GameMap.polygons_array[ActivePolygonNum] = copy.deepcopy(ActivePolygon)
	ActivePolygon = None
	NewActivePolygon = None
	FreezedPoint = None
	ActivePoint = None
	ActivePolygonNum = None
	StartAngle = None
	AngleNow = None

def print_mouse(mouse_pos):
	strng = "mouse: " + str(mouse_pos)
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

def get_norm_delta(start,finish):
	# start, finish - gradus
	## delta < 0:поворот вправо; >0:поворот влево
	if start*finish>0:
		d = start - finish
	else:
		new_angle_1 = math.asin(math.sin(start*pi/180))*180/pi
		new_angle_2 = math.asin(math.sin(finish*pi/180))*180/pi
		d = abs(new_angle_1)+abs(new_angle_2)
		print 'new_angle_1 ',new_angle_1
		print 'new_angle_2 ',new_angle_2
		if (not(abs(start)>90) and (finish>0)) or ((abs(start)>90) and not (finish>0)):
			d *= -1
		print 'Indelta ',d
	return -d

while 1:
	# draw background and coordinate grid
	windowSurfaceObj.fill(whitecolor)
	windowSurfaceObj.blit(GameMap.redraw(),(0,0))
	
	# можем ли двигать текущий полигон
	if GameMap.Mode == MOVE:
		# вычисление текущего угла
		descaledmxy = [mousexy[0]/float(GameMap.Scale),mousexy[1]/float(GameMap.Scale)]
		AngleNow = GameMap.get_start_angle(ActivePolygon,descaledmxy,FreezedPoint)
		if MLOG: print ''
		if MLOG: print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
		if MLOG: print ''
		if MLOG: print 'Mouse: ',descaledmxy ,'; angle: ',AngleNow, '; FreezedPoint: ',FreezedPoint,'; NewActivePolygon: ',NewActivePolygon
		# возможность двинуть полигон
		if 1:
			# поворот влево - <0
			delta = get_norm_delta(StartAngle,AngleNow)
			if MLOG: print 'AngleNow ',AngleNow
			if MLOG: print 'StartAngle ' ,StartAngle
			if MLOG: print " Delta: ",delta,", FP: ", FreezedPoint
			tmp_FP = FreezedPoint[:]
			tmp_AP = copy.deepcopy(ActivePolygon)
			NewActivePolygon = copy.deepcopy(ActivePolygon.rotate(delta,FreezedPoint[:]))
			ActivePolygon = copy.deepcopy(tmp_AP)
			FreezedPoint = tmp_FP[:]
			del tmp_FP
			del tmp_AP
			if MLOG: print " After Delta: ",delta,", FP: ", FreezedPoint
			# print 'NewActivePolygon = ',NewActivePolygon
			# проверка на 90-градусный поворот
			if (abs(delta)>90-MAX_ANGLE_DELTA):
				print 'REWRITED!'
				# перезапись полигона StartPolyg
				ActivePolygon = ActivePolygon.rotate((abs(delta)/delta)*90,FreezedPoint)
				StartAngle = StartAngle + sign(delta)*90 
				if StartAngle >= 180:
					StartAngle -= 360
				if StartAngle < -180:
					StartAngle += 360
				print 'New StartAngle = ',StartAngle
			# перезапись GameMap полигона
			GameMap.polygons_array[ActivePolygonNum] = copy.deepcopy(NewActivePolygon)
			# перерисовка полигона

	if MLOG: pgn,pnt = GameMap.mouse_near_corner(mousexy,r=SensorRadius)
	if MLOG and not(pnt==None) and not(pgn == None):
		oc = GameMap.get_oppose_corner(pgn,pnt)
		pygame.draw.circle(windowSurfaceObj, greencolor, [int(pnt[0]*GameMap.Scale),int(pnt[1]*GameMap.Scale)], SensorRadius,3)
		pygame.draw.circle(windowSurfaceObj, redcolor,   [int(oc[0]*GameMap.Scale),int(oc[1]*GameMap.Scale)], SensorRadius,3)
		GameMap.get_start_angle(pgn,pnt)
	if MLOG: print_mouse(mousexy)	

	# get events
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

		elif event.type == MOUSEBUTTONDOWN:
			mousexy = pygame.mouse.get_pos()
			# 1 - LB 2 - MB 3 - RB 4 - SU 5 - SD
			if (event.button == 1) and (GameMap.Mode == CHOOSE):
				GameMap.Mode = MOVE
				ActivePolygon, ActivePoint = GameMap.mouse_near_corner(mousexy,r=SensorRadius)
				if (ActivePolygon==None) or (ActivePoint == None):
					GameMap.Mode = CHOOSE
					ActivePolygon, ActivePoint = None, None
				else:
					FreezedPoint = GameMap.get_oppose_corner(ActivePolygon,ActivePoint)
					ActivePolygonNum = GameMap.polygons_array[:].index(ActivePolygon)
					# print ActivePolygonNum
					StartAngle = GameMap.get_start_angle(ActivePolygon,ActivePoint)
					AngleNow = copy.deepcopy(StartAngle)
					NewActivePolygon = copy.deepcopy(ActivePolygon)
			
		elif event.type == MOUSEMOTION:
			mousexy = pygame.mouse.get_pos()

		elif event.type == MOUSEBUTTONUP:
			mousexy = pygame.mouse.get_pos()
			if event.button == 1:
				mouse_button_up()

	pygame.display.update()
	fpsClock.tick(30)