# -*- coding: utf-8 -*-
from Parser import Parser

class CountryCheckFlagParser(Parser):
	def __init__(self):
		super(CountryCheckFlagParser, self).__init__(r"^checkflag\((http://[0-9a-zA-Z_.]*[gif|jpeg])\)$")

	def __call__(self, query):
		if self.wrapper(self.regex.match(query)):
			return self.__parse(self.wrapper.match.group(1))
		else:
			return False

	def __parse(self, url):
		pass
		