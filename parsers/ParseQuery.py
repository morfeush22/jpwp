# -*- coding: utf-8 -*-
from parsers import CountryParser, CountryTagParser, CountryJsonParser, CountryGetFlagParser, CountryCheckFlagParser
from PIL import Image
from MakeRequest import MakeRequest

import base64
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
		if query == "exit":
			sys.exit()

		for parser in self.parsers:
			try:
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
						response = self.requestMaker(result)
						if response[1] == "media":
							decoded = base64.b64decode(response[0])
							image = Image.open(io.BytesIO(decoded))
							image.show()
							return True
						elif response[1] == "data":
							print response[0]
							return True

			except ValueError as e:
				print repr(e)
			except UserWarning:
				raise

		raise UserWarning("Wrong query!")

	def parseHttpRequest(self, queryType, query):
		for parser in self.dataParsers + self.mediaParsers:
			match = parser.match(query)
			if match:
				if queryType == "media" and parser in self.mediaParsers:
					if parser is self.countryGetFlagParser:
						return {"response": base64.b64encode(parser(query)), "type": "media"}
					else:
						return {"response": parser(query), "type": "data"}
				elif queryType == "data" and parser in self.dataParsers:
					return {"response": parser(query), "type": "data"}
				else:
					return {"response": "Type mismatch!", "type": "data"}

		return {"response": "Wrong query!", "type": "data"}
		