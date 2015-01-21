# -*- coding: utf-8 -*-
from parsers import CountryParser, CountryTagParser, CountryJsonParser, CountryGetFlagParser, CountryCheckFlagParser
from MakeRequest import MakeRequest

import sys

class ParseQuery(object):
	def __init__(self, db):
		self.countryParser = CountryParser(db)
		self.countryTagParser = CountryTagParser(self.parseQuery)
		self.countryJsonParser = CountryJsonParser()
		self.countryGetFlagParser = CountryGetFlagParser()
		self.countryCheckFlagParser = CountryCheckFlagParser()
		self.requestMaker = MakeRequest()

		self.dataParsers = [self.countryParser, \
			self.countryTagParser]

		self.mediaParsers = [self.countryGetFlagParser, \
			self.countryCheckFlagParser]

		self.parsers = self.dataParsers + self.mediaParsers
		
	def parseQuery(self, query):
		for parser in self.parsers:
			result = parser(query)
			if result != False:
				return result

		result = self.countryJsonParser(query)
		if result != False:
			return self.requestMaker(result)
		
		if query == "exit":
			sys.exit()

		raise ValueError("Wrong query!")

	def parseHttpRequest(self, queryType, query):
		for parser in self.parsers:
			match = parser.match(query)
			if match:
				if queryType == "media" and parser in self.mediaParsers:
					return {"response": "Media!"}
				elif queryType == "data" and parser in self.dataParsers:
					return {"response": parser(query)}
				else:
					return {"response": "Type mismatch!"}

		return {"response": "Wrong query!"}
		