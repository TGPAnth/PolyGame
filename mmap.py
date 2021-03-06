# -*- coding: utf-8 -*-

import pygame, sys, math, copy
from pygame.locals import *
from poly import *
pygame.init()

LOG = 0
CHOOSE = 0
mMOVE = 1


class Map():
	def __init__(self,wd,hg):
		self.polygons_array = []
		self.finish_array = []
		self.height = 10
		self.width = 10
		self.Draw_Coord = 1
		self.Scale = 32 #""" TODO: """# Расчитывать ДИНАМИЧЕСКИ!!!
		self.wd = wd
		self.hg = hg
		self.Surface = pygame.Surface((wd,hg))
		self.coord_color = (0,0,0)
		self.coord_line_wd = 1
		self.poly_wd = 4
		self.bkgnd_color = (255,255,255)
		self.Mode = CHOOSE
		self.ActivePolygonNum = None
		self.ActivePolygon = None
		self.NewActivePolygon = None
		self.FreezedPoint = None
		self.ActivePoint = None
		self.StartAngle = None
		self.AngleNow = None
		self.ActivePointNum = None
		self.delta_prev = None
		self.Level = 0

	def load_level(self,lst):
		for i in lst:
			print i
			self.add(Polygon(*i))
		return True

	def get_AS(self):
		return self.Mode

	def redraw(self):
		self.Surface = pygame.Surface((self.wd,self.hg))
		self.Surface.fill(self.bkgnd_color)
		if self.Draw_Coord: self.redraw_coord()
		for i in self.polygons_array:
			self.redraw_poly(i)
		for i in self.finish_array:
			self.redraw_poly(i)
		return self.Surface

	def in_radius(self,xy,mxy,r):
		return (mxy[0] - xy[0])**2 + (mxy[1] - xy[1])**2 <= r**2

	def mouse_near_corner(self,mxy,r=3):
		for p in self.polygons_array[:]:
			if not(p.can_move()):
				continue
			for point in p[:]:
				if self.in_radius([point[0]*self.Scale,point[1]*self.Scale],mxy,r):
					self.ActivePolygon, self.ActivePoint = copy.deepcopy(p),point[:]
					return None
		self.ActivePolygon, self.ActivePoint 

	def gradus2rad(self,a):
		return a*pi/180

	def rad2gradus(self,a):
		return a*180/pi

	def get_oppose_corner(self,polyg,point):
		num = polyg[:].index(point)
		num += 2
		if num >= len(polyg[:]):
			num -= len(polyg[:])
		self.FreezedPoint = polyg[num][:]
		return self.FreezedPoint

	def sign(self,a):
		if a<0:
			return -1
		return 1

	def get_start_angle(self,APolyg = None,APoint = None,FPoint = None):
		if APolyg == None:
			APolyg = self.ActivePolygon
		if APoint == None:
			APoint = self.ActivePoint
		if FPoint == None:
			FPoint = self.get_oppose_corner(APolyg,APoint)
		self.StartAngle = self.get_angle(APolyg,APoint,FPoint)

	def get_now_angle(self,APolyg = None,APoint = None,FPoint = None):
		if APolyg == None:
			APolyg = self.ActivePolygon
		if APoint == None:
			APoint = self.ActivePoint
		if FPoint == None:
			FPoint = self.get_oppose_corner(APolyg,APoint)
		self.AngleNow = self.get_angle(APolyg,APoint,FPoint)

	def get_angle(self,polyg,act_pnt,freeze_pnt,dlta = 0.001):
		# print '!!!!',polyg,act_pnt,freeze_pnt
		params = polyg.get_parameters(act_pnt,freeze_pnt)
		pA = params[0]
		pB = params[1]
		if abs(pB)<=dlta:
			return self.sign(pA)*90.0
		if abs(pA)<=dlta:
			return self.sign(pB)*90.0 - 90
		angle = math.atan(-1*params[0]/float(params[1]))
		if LOG: print act_pnt,' ',polyg.rad2gradus(angle),' ',angle,' ',params[0]/float(params[1])
		angle = self.rad2gradus(angle)
		# params = polyg.get_parameters(act_pnt,freeze_pnt)
		if ((pA>0)and(pB<0))or((pA<0)and(pB<0)):
			angle = self.sign(angle)*(180-abs(angle))
		else:
			angle *= -1
		return angle


	def redraw_coord(self):
		for i in xrange(0,self.wd,self.Scale):
			pygame.draw.line(self.Surface, self.coord_color, (i,0), (i,self.hg), self.coord_line_wd )
		for i in xrange(0,self.hg,self.Scale):
			pygame.draw.line(self.Surface, self.coord_color, (0,i), (self.wd,i), self.coord_line_wd )

	def redraw_poly(self,polyg):
		# print [[i[0]*self.Scale,i[1]*self.Scale] for i in polyg[:]]
		pygame.draw.polygon(self.Surface, polyg.type, [[i[0]*self.Scale,i[1]*self.Scale] for i in polyg[:]], self.poly_wd)

	def add(self,polyg,polyg_type = None):
		if polyg_type in (WALL, FINISH, MOVE):
			# print polyg_type
			# # print MOVE
			if polyg_type == MOVE:
				polyg.move = 1
			polyg.type = polyg_type
		if polyg.type == FINISH:
			self.finish_array.append(polyg)
			return True
		self.polygons_array.append(polyg)
		return True

	def get_index(self,polyg):
		j = 0
		for x in xrange(len(polyg[:])):
			if polyg[x]==self.ActivePoint:
				self.ActivePointNum = x
		for i in self.polygons_array[:]:
			if i.__dict__ == polyg.__dict__:
				self.ActivePolygonNum = j
				return None
			j += 1
		self.ActivePolygonNum = None

	def sign(self,a):
		if a<0:
			return -1
		return 1

	def get_norm_delta(self,start,finish):
		# start, finish - gradus
		## delta < 0:поворот вправо; >0:поворот влево
		if start*finish>0:
			d = start - finish
		else:
			new_angle_1 = math.asin(math.sin(start*pi/180))*180/pi
			new_angle_2 = math.asin(math.sin(finish*pi/180))*180/pi
			d = new_angle_1 - new_angle_2
			if LOG: print 'new_angle_1 ',new_angle_1
			if LOG: print 'new_angle_2 ',new_angle_2
			# d = abs(new_angle_1)+abs(new_angle_2)
			# if (not(abs(start)>90) and (finish>0)) or ((abs(start)>90) and not (finish>0)):
			# 	d *= -1
			if abs(start)>90 and abs(finish)>90:
				d*= -1
			if LOG: print 'Indelta ',d
		return -d

	def not_intersecs(self,delta):
		# print '\n\n START CHECK \n'
		f = lambda a=self.FreezedPoint,b=self.ActivePoint:math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)
		for i in self.polygons_array[:]:
			if i[:] == self.NewActivePolygon[:]:
				continue
			# print i
			if i.cross(self.NewActivePolygon,self.ActivePoint):
				if LOG: print ' !!!!!!!!!!!! FAIL !!!!!!!!!!!!'
				return False
		return True

	def move_polygons(self,msxy,MAD):
		# вычисление текущего угла
		descaledmxy = [msxy[0]/float(self.Scale),msxy[1]/float(self.Scale)]
		self.get_now_angle(self.ActivePolygon,descaledmxy,self.FreezedPoint)
		del descaledmxy
		delta = 1*self.get_norm_delta(self.StartAngle,self.AngleNow)
		# print self.AngleNow,'                  ',delta
		# возможность двинуть полигон
		if self.not_intersecs(delta):
		# 	pass
		# if 1:
			# поворот влево - <0
			tmp_AP = copy.deepcopy(self.ActivePolygon)
			self.NewActivePolygon = copy.deepcopy(tmp_AP.rotate(delta,self.FreezedPoint[:]))
			del tmp_AP
			# проверка на 90-градусный поворот
			if (abs(delta)>90-MAD):
				# перезапись полигона StartPolyg
				self.ActivePolygon.rotate((abs(delta)/delta)*90,self.FreezedPoint,new = False)
				self.ActivePoint = self.ActivePolygon[self.ActivePointNum][:]
				self.get_start_angle()
				if self.StartAngle >= 180:
					self.StartAngle -= 360
				if self.StartAngle < -180:
					self.StartAngle += 360
			del delta
			# перезапись self полигона
			self.polygons_array[self.ActivePolygonNum] = copy.deepcopy(self.NewActivePolygon)
			# перерисовка полигона
			return True
		else:
			return False

	def parse_cursor(self,string, hotspot=(0, 0), and_xor=True, outline="1", fill="0",bg=" "):
		"""A light-weight cursor parser.

		Takes a multi-line string as a cursor map, and converts it into an arg set
		for `pygame.mouse.set_cursor`.

		:param string: The multi-line cursor bit-map.
		:type string: str
		:param hotspot: Coordinates for cursor's hotspot.
		:type hotspot: tuple
		:param and_xor: Whether or not to and the outlining 'xor' bits (makes out-
		line static).
		:type and_xor: bool
		:param outline: Token representing the outline in within the map string.
		:type outline: str
		:param fill: Token representing filled pixels within the map string.
		:type fill: str
		:param bg: Token representing the background, or transparent pixels of the
		map string.
		:type bg: str
		:return: Set of data to unpack as args for `pygame.mouse.set_cursor` func.
		:rtype: tuple
		"""
		# Initialize with empty tuples
		xormask = tuple()
		andmask = tuple()
		# Convert string to bitstrings
		if not and_xor:
			andstr = string.replace(outline, bg)
		else:
			andstr = string.replace(outline, "1")
		xorstr = string.replace(bg, "0").replace(fill, "0").replace(outline, "1")
		andstr = string.replace(fill, "1").replace(bg, "0")
		# Parse lines for xormask
		lines = [l for l in xorstr.split('\n') if l != ""]
		# ---- Width check
		if len(lines[0]) % 8 != 0:
			return None
		b = len(lines[0]) / 8
		for line in lines:
			xormask += tuple([int(line[i * 8:(i + 1) * 8], 2) for i in xrange(b)])
		# Parse lines for andmask
		lines = [l for l in andstr.split('\n') if l != ""]
		for line in lines:
			andmask += tuple([int(line[i * 8:(i + 1) * 8], 2) for i in xrange(b)])
		# return complete argset for set_cursor
		return ((len(lines[0]), len(lines)), hotspot, xormask, andmask)

	def set_cursor(self,cursor):
		"""Sets mouse cursor."""
		if cursor is None:
			return False
		pygame.mouse.set_cursor(*cursor)
		return True

	def init_cursor(self):
		cur_str_hand = '''
		     11         
		    1001        
		    1001        
		    1001        
		    10011       
		    10010111    
		    1001001011  
		    10010010011 
		111 100100100101
		1001100000000101
		1000100000000001
		 100100000000001
		  10000000000001
		  10000000000001
		   1000000000001
		   100000000001 
		    10000000001 
		     100000001  
		     100000001  
		     111111111  
		'''
		cursor_hand = self.parse_cursor(cur_str_hand, (5, 0))

		cur_str_default = '''
		#---------------
		##--------------
		#*#-------------
		#**#------------
		#***#-----------
		#****#----------
		#*****#---------
		#******#--------
		#*******#-------
		#********#------
		#*****#####-----
		#**#**#---------
		#*#-#**#--------
		##--#**#--------
		#----#**#-------
		-----#**#-------
		------#**#------
		------#**#------
		-------##-------
		'''
		# cursor_default = self.parse_cursor(cur_str_default, outline="#", fill="*", bg="-")
		self.set_cursor(cursor_hand)
