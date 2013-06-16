# -*- coding: utf-8 -*-

class Menu(object):

	def __init__(self):
		self.languages = ['en','ru']
		self.default_lang = 'en'
		self.menu_list = get_language()

	def get_menu_list(self):
		return self.menu_list

	""" Получаем язык меню """
	def get_language(self,lang = None):
		if lang == None: lang = self.default_lang
		menu_list_all_lang = []
		menu_list_all_lang.append(['en','Start','Choose Level','Options','Exit'])
		menu_list_all_lang.append(['ru','Поехали','Выбрать уровень','Опции','Выход'])
		print menu_list_all_lang
		try: return [x[1:] for x in menu_list_all_lang if x[0]==lang][0]
		except: return menu_list_all_lang[0][1:]

n = Menu()
print n.get_language()