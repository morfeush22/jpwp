# -*- coding: utf-8 -*-
from Parser import Parser

class CountryGetFlagParser(Parser):
	def __init__(self):
		super(CountryGetFlagParser, self).__init__(r"^country\(([a-zA-Z\s]*)\);\s*getflag$")
		
	def __call__(self, query):
		if self.wrapper(self.regex.match(query)):
			return self.__parse(self.replaceTabs("_", self.wrapper.match.group(1)))
		else:
			return False

	def __parse(self, country):
		pass
