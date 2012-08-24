# -*- coding: utf-8 -*-

import pygame, sys, math
from pygame.locals import *
from poly import *
pygame.init()

LOG = 0
CHOOSE = 0
MOVE = 1


class Map():

	def __init__(self,wd,hg):
		self.polygons_array = []
		self.height = 10
		self.width = 10
		self.Draw_Coord = 1
		self.Scale = 32
		self.wd = wd
		self.hg = hg
		self.Surface = pygame.Surface((wd,hg))
		self.coord_color = (0,0,0)
		self.coord_line_wd = 1
		self.poly_wd = 4
		self.bkgnd_color = (255,255,255)
		self.Mode = CHOOSE

	def redraw(self):
		self.Surface = pygame.Surface((self.wd,self.hg))
		self.Surface.fill(self.bkgnd_color)
		if self.Draw_Coord: self.redraw_coord()
		for i in self.polygons_array:
			self.redraw_poly(i)
		return self.Surface

	def in_radius(self,xy,mxy,r):
		return (mxy[0] - xy[0])**2 + (mxy[1] - xy[1])**2 <= r**2

	def mouse_near_corner(self,mxy,r=3):
		for p in self.polygons_array:
			# if not(p.move):
			# 	continue
			for point in p[:]:
				if self.in_radius([point[0]*self.Scale,point[1]*self.Scale],mxy,r):
					return p,point[:]
		return None,None

	def gradus2rad(self,a):
		return a*pi/180

	def rad2gradus(self,a):
		return a*180/pi

	def get_oppose_corner(self,polyg,point):
		num = polyg[:].index(point)
		num += 2
		if num >= len(polyg[:]):
			num -= len(polyg[:])
		return polyg[num]

	def sign(self,a):
		if a<0:
			return -1
		return 1

	def get_start_angle(self,polyg,act_pnt,freeze_pnt = None):
		if freeze_pnt == None:
			freeze_pnt = self.get_oppose_corner(polyg,act_pnt)
		params = polyg.get_parameters(act_pnt,freeze_pnt)
		if abs(params[1])<=0.001:
			return 90.0
		angle = math.atan(-1*params[0]/float(params[1]))
		if LOG: print act_pnt,' ',polyg.rad2gradus(angle),' ',angle,' ',params[0]/float(params[1])
		angle = self.rad2gradus(angle)
		params = polyg.get_parameters(act_pnt,freeze_pnt)
		pA = params[0]
		pB = params[1]
		if ((pA>0)and(pB<=0))or((pA<0)and(pB<0)):
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
		pygame.draw.polygon(self.Surface, polyg.color, [[i[0]*self.Scale,i[1]*self.Scale] for i in polyg[:]], self.poly_wd)

	def add(self,polyg):
		self.polygons_array.append(polyg)

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