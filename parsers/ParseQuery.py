# -*- coding: utf-8 -*-
from parsers import CountryParser, CountryTagParser, CountryJsonParser, CountryGetFlagParser, CountryCheckFlagParser
from PIL import Image
from MakeRequest import MakeRequest

import io
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

		self.parsers = self.dataParsers + self.mediaParsers + [self.countryJsonParser]
		
	def parseQuery(self, query):
		for parser in self.parsers:
			result = parser(query)
			if result != False:
				if parser in self.dataParsers + [self.countryCheckFlagParser]:
					print result
					return True
				elif parser is self.countryGetFlagParser:
					image = Image.open(io.BytesIO(result))
					image.show()
					return True
				else:
					print self.requestMaker(result)
					return True			
		
		if query == "exit":
			sys.exit()

		raise ValueError("Wrong query!")

	def parseHttpRequest(self, queryType, query):
		for parser in self.dataParsers + self.mediaParsers:
			match = parser.match(query)
			if match:
				if queryType == "media" and parser in self.mediaParsers:
					return {"response": "Media!"}
				elif queryType == "data" and parser in self.dataParsers:
					return {"response": parser(query)}
				else:
					return {"response": "Type mismatch!"}

		return {"response": "Wrong query!"}
		