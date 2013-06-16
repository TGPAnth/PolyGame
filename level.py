# -*- coding: utf-8 -*-
from poly import *
class Level(object):

	def __init__(self):
		self.levels = self.default_level_list()

	def default_level_list(self):
		lvls = []
		lvl1 = []
		lvl1.append([[[1,1],[18,1],[18,14],[1,14]],WALL])
		lvl1.append([[[2,2],[5,2],[5,5],[2,5]],WALL])
		lvl1.append([[[11,5],[11,2],[17,2],[17,5]],WALL])
		lvl1.append([[[2,6],[3,6],[3,12],[2,12]],WALL])
		lvl1.append([[[11,6],[15,6],[15,8],[11,8]],WALL])
		lvl1.append([[[15,9],[17,9],[17,13],[15,13]],WALL])
		lvl1.append([[[6,3],[10,3],[10,5],[6,5]],MOVE])
		lvl1.append([[[10,11],[14,11],[14,13],[10,13]],FINISH])
		lvls.append(lvl1)
		return lvls	

	def levels_num(self):
		return len(self.levels)

	def get_levels(self):
		pass

	def load_level_list(self):
		pass

	def save_level_list(self):
		pass

	def get_level_pict(self):
		pass

	def create_level_pict(self):
		pass

	def test_level_picts(self):
		pass
		
	def function():
		pass

	def __getslice__(self, i, j):
		return self.levels[i:j]

	# def __nonzero__(self):
	# 	if len(self.pts)>3:
	# 		return True
	# 	return False

	# def __str__(self):
	# 	st = "Polygon: "+ str(self.pts)
	# 	return st

	# def __contains__(self,item):
	# 	return item in self.pts

	def __getitem__(self,num):
		# print self.levels
		return self.levels[num]