# -*- coding: utf-8 -*-
from Parser import Parser

class CountryGetFlagParser(Parser):
	def __init__(self):
		super(CountryGetFlagParser, self).__init__(r"^country\(([a-zA-Z]*)\);?getflag$")
		