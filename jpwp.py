# -*- coding: utf-8 -*-
# ylnvsspc
# ylnvsspc1
from parsers import CountryParser, CountryTagParser, CountryJsonParser, CountryGetFlagParser, CountryCheckFlagParser
from pymongo import MongoClient

import re

class ParseQuery(object):
	def __init__(self, db):
		self.countryParser = CountryParser(db)
		self.countryTagParser = CountryTagParser(self.__call__)
		self.countryJsonParser = CountryJsonParser(self.__call__)
		self.countryGetFlagParser = CountryGetFlagParser()
		self.countryCheckFlagParser = CountryCheckFlagParser()

		self.parsers = [self.countryParser, \
			self.countryTagParser, \
			self.countryJsonParser, \
			self.countryGetFlagParser, \
			self.countryCheckFlagParser]
		
	def __call__(self, query):
		for _parser in self.parsers:
			_result = _parser(query)
			if _result != False:
				return _result

		raise ValueError("Wrong query!")

if __name__ == "__main__":
	_client = MongoClient("mongodb://admin:admin@ds056727.mongolab.com:56727/countries")
	_db = _client.countries
	_queryParser = ParseQuery(_db)

	while True:
		print "Enter query:"
		print _queryParser(re.sub(r"\s+", "", raw_input().lower()))
