# -*- coding: utf-8 -*-

from math import sin,cos,tan,pi

LOG = 0
MOVE = (255,0,0)
WALL = (0,0,0)
FINISH = (0,255,0)

class Polygon():
	
	def __init__(self,lst):
		self.pts = []
		if self.is_poly(lst):
			self.pts = lst[:]
			# for i in xrange(len(self.pts)):
			# 	self.pts[i] = [int(self.pts[i][0]),int(self.pts[i][1])]
		self.move = 1
		self.color = WALL

	def parallel_axes(self,lst):
		if lst[0]!=lst[-1]:lst.append(lst[0])
		for i in xrange(len(lst)-1):
			if not((lst[i][0]==lst[i+1][0]) or (lst[i][1]==lst[i+1][1])):
				return False
		return True

	def is_poly(self,a):
		if not (isinstance(a,list)):
			if LOG: print 'Not list!'
			return False
		if not(len(a)==4):
			if LOG: print 'Length is not 4'
			return False
		# if not(self.parallel_axes(a[:])):
		# 	if LOG: print 'Is not parallel'
		# 	return False
		return True

	def gradus2rad(self,a):
		return a*pi/180

	def rad2gradus(self,a):
		return a*180/pi

	def rotate_point(self,xy,a=None,only_x = 0,only_y = 0):
		"""
		a - radian! NOT tan(alpha)
		"""
		if a == None:
			return xy
		x = xy[0]
		y = xy[1]
		cosa = round(cos(a),4)
		sina = round(sin(a),4)
		new_x = x*cosa + y*sina
		new_y = -1*x*sina+y*cosa
		if only_x : return new_x
		if only_y : return new_y
		return [new_x,new_y]

	def intersec_with_arc(self,x0,y0,r,angle_start,angle_finish,every = 2):
		
		def get_xy(x,y,rq,angle):
			uy = round(y + cos(angle)*rq,3)
			ux = round(x + sin(angle)*rq,3)
			return [uy,ux]

		delta_angle = abs(angle_start - angle_finish)
		min_angle = min([angle_start,angle_finish])
		max_angle = max([angle_start,angle_finish])
		angles = [x+min_angle for x in xrange(delta_angle+1) if x%every]
		coords = [get_xy(x0,y0,r,self.gradus2rad(i)) for i in angles]
		if LOG:
			print '>>>>>>  intersec_with_arc  >>>>>> '
			print 'x0 = ',x0,', y0 = ',y0,', r = ',r
			print angles
			print coords
			print 'min_angle = ',min_angle,', max_angle = ',max_angle
			print '[coord] --- [angle] '
			for o in xrange(len(angles)):
				print angles[o], ' - ',coords[o]
			print '<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'
		for x in xrange(len(coords)-1):
			if self.cross_with_line(coords[x],coords[x+1]):
				return True
		return False

	def rotate(self,angle=None,nullpoint = None):
		# angle - gradus
		def sgn(a):
			if a<0:
				return -1
			return 1

		def normalize(a):
			if not(-90<=a<=90):
				angle = (abs(a)-90)*sgn(a)
				normalize(a)
			return True

		def to_zero(g=None,np = None):
			a = g[:]
			if np == None:
				f = a[0]
			else:
				f = np[:]
			for i in xrange(len(a)):
				if LOG: print 'i :',i,' a[i]: ',a[i],' a: ',a,' f: ',f
				a[i][0] -= f[0]
				a[i][1] -= f[1]
			del g,np
			return a[:],f
		
		def from_zero(a=None,f=None):
			for i in xrange(len(a)):
				a[i][0] +=f[0]
				a[i][1] +=f[1]
			return a[:]

		if angle < 0: angle+=360
		a1 = self.pts[:]
		if LOG: print 'A ',a1,' nullpoint = ',nullpoint
		g,h = to_zero(a1[:], np = nullpoint)
		if LOG: print 'Start = ',g,' ',h,' NP=',nullpoint
		for i in xrange(len(g)):
			g[i] = self.rotate_point(g[i],self.gradus2rad(angle))
		if LOG: print 'NewG = ',g,' NP=',nullpoint
		j = from_zero(g[:],h[:])
		if LOG: print 'ForNP ',j,' NP=',nullpoint
		pgn = Polygon(j[:])
		pgn.move = self.move
		pgn.color = self.color
		if LOG: print 'PGN ',pgn,' NP=',nullpoint
		del a1,g,h,j,nullpoint
		return pgn

	def rewrite_pts(self,a):
		if not (self.is_poly(a)):
			return False
		self.pts = a[:]
		return True

	def __nonzero__(self):
		if len(self.pts)>3:
			return True
		return False

	def __str__(self):
		st = "Polygon: "+ str(self.pts)
		return st

	def __contains__(self,item):
		return item in self.pts

	def __getitem__(self,num):
		return self.pts[num]

	def contain(self,item):
		if len(item)!=2:
			return False
		x = item[0]
		y = item[1]
		minx = min([x for x,y in self.pts])
		miny = min([y for x,y in self.pts])
		maxx = max([x for x,y in self.pts])
		maxy = max([y for x,y in self.pts])
		if (minx<=x<=maxx) and (miny<=y<=maxy):
			return True
		return False

	def find_A(self,XY1,XY2):
		return XY2[1]-XY1[1]

	def find_B(self,XY1,XY2):
		return -XY2[0]+XY1[0]

	def find_C(self,XY1,XY2):
		# dx = XY2[0]-XY1[0]
		# dy = XY2[1]-XY1[1]
		return -XY1[0]*XY2[1]+XY2[0]*XY1[1]

	def get_parameters(self,XY1,XY2):
		return [self.find_A(XY1,XY2),self.find_B(XY1,XY2),self.find_C(XY1,XY2)]

	def cross(self,a):
		a1 = self.pts[:]
		a2 = a[:]
		if a1[0]!=a1[-1]:a1.append(a1[0])
		if a2[0]!=a2[-1]:a2.append(a2[0])
		for i in xrange(len(a1)-1):
			for j in xrange(len(a2)-1):
				if self.cross_line(a1[i],a1[i+1],a2[j],a2[j+1]):
					return True
		return False

	def cross_with_line(self,xy,xy1):
		a1 = self.pts[:]
		if a1[0]!=a1[-1]:a1.append(a1[0])
		for i in xrange(len(a1)-1):
			if LOG:
				print '>>>>> cross_with_line >>>>>'
				print  a1[i],a1[i+1],xy,xy1
				print '<<<<<<<<<<<<<<<<<<<<<<<<<<<'
			if self.cross_line(a1[i],a1[i+1],xy,xy1):
				return True
		return False

	def cross_line(self,A1,A2,B1,B2):
		if self.line_on_line_cross(A1,A2,B1,B2):
			if LOG: print '!!! line_on_line_cross = ',A1,A2,B1,B2
			return False #???
		if self.line_on_line(A1,A2,B1,B2):
			if LOG: print '!!! line_on_line = ',A1,A2,B1,B2
			return False	
		if self.parallel_lines(A1,A2,B1,B2):
			if LOG: print '!!! parallel_lines = ',A1,A2,B1,B2
			return False
		a = self.cross_point(A1,A2,B1,B2)
		if LOG: 
			print '... cross_point = ',a
			print '... between(A1,A2,a)',self.between(A1,A2,a),A1,A2,a
			print '... between(B1,B2,a)',self.between(B1,B2,a),B1,B2,a
		return self.between(A1,A2,a) and self.between(B1,B2,a)

	def cross_point(self,aXY1,aXY2,bXY1,bXY2):
		"""
		Ax + By + C = 0
		"""
		A1 = self.find_A(aXY1,aXY2)
		A2 = self.find_A(bXY1,bXY2)
		B1 = self.find_B(aXY1,aXY2)
		B2 = self.find_B(bXY1,bXY2)
		C1 = self.find_C(aXY1,aXY2)
		C2 = self.find_C(bXY1,bXY2)
		# print [A1,B1,C1],[A2,B2,C2]
		if (A1==A2==0) or (B1==B2==0):
			return None
		return [(B1*C2-B2*C1)/float(A1*B2-A2*B1),(C1*A2-C2*A1)/float(A1*B2-A2*B1)]
	
	def cross_point_param(self,lt1,lt2):
		A1 = lt1[0]
		A2 = lt2[0]
		B1 = lt1[1]
		B2 = lt2[1]
		C1 = lt1[2]
		C2 = lt2[2]
		if A1*B2-A2*B1 == 0:
			return None
		return [(B1*C2-B2*C1)/float(A1*B2-A2*B1),(C1*A2-C2*A1)/float(A1*B2-A2*B1)]

	def between(self,A1,A2,XY):
		return ((((XY[0]-A1[0])**2+(XY[1]-A1[1])**2)**(1.0/2)) + (((A2[0]-XY[0])**2+(A2[1]-XY[1])**2)**(1.0/2))) / float(((A2[0]-A1[0])**2+(A2[1]-A1[1])**2)**(1.0/2)) <= 1.1

	def on_line(self,A1,A2,XY):
		return (0.01 >= (XY[1] - A1[1]) * (A2[0] - A1[0]) - (XY[0] - A1[0]) * (A2[1] - A1[1]))

	def line_on_line(self,A1,A2,B1,B2):
		if self.on_line(A1,A2,B1) and self.on_line(A1,A2,B2):
			return True
		return False
	
	def line_on_line_cross(self,A1,A2,B1,B2):
		if self.line_on_line(A1,A2,B1,B2) and (self.between(A1,A2,B1) or self.between(A1,A2,B2) or self.between(B1,B2,A1) or self.between(B1,B2,A2)):
			return True
		return False

	def parallel_lines(self,aXY1,aXY2,bXY1,bXY2):
		"""
		Ax + By + C = 0
		"""
		A1 = self.find_A(aXY1,aXY2)
		A2 = self.find_A(bXY1,bXY2)
		B1 = self.find_B(aXY1,aXY2)
		B2 = self.find_B(bXY1,bXY2)
		C1 = self.find_C(aXY1,aXY2)
		C2 = self.find_C(bXY1,bXY2)
		# print [A1,B1,C1],[A2,B2,C2]
		if A1*B2 == A2*B1:
			return True
		return False

	def __getslice__(self, i, j):
		return self.pts[i:j]