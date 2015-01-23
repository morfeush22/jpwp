# -*- coding: utf-8 -*-
from Parser import Parser

import requests

class CountryGetFlagParser(Parser):
	def __init__(self):
		super(CountryGetFlagParser, self).__init__(r"^country\(([a-zA-Z\s]*)\);\s*getflag$")
		
	def __call__(self, query):
		if self.wrapper(self.regex.match(query)):
			return self.__parse(self.replaceTabs("-", self.wrapper.match.group(1).strip()))
		else:
			return False

	def __parse(self, country):
		url = "http://www.mapsofworld.com/images/world-countries-flags/" + country + "-flag.gif"
		req = requests.get(url, stream=True)

		req.raise_for_status()

		req.raw.decode_content = True

		return req.raw.read()
