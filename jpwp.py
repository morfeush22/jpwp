# -*- coding: utf-8 -*-
# ylnvsspc
# ylnvsspc1
from parsers import CountryParser, CountryTagParser, CountryJsonParser, CountryGetFlagParser, CountryCheckFlagParser
from pymongo import MongoClient
from threading import Thread

import re
import sys
import tornado.escape
import tornado.ioloop
import tornado.web

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
		
		if query == "exit":
			sys.exit()

		raise ValueError("Wrong query!")

class RequestHandler(tornado.web.RequestHandler):
	def post(self):
		data = tornado.escape.json_decode(self.request.body)
		self.write(data)

if __name__ == "__main__":
	_client = MongoClient("mongodb://admin:admin@ds056727.mongolab.com:56727/countries")
	_db = _client.countries
	_queryParser = ParseQuery(_db)

	if len(sys.argv) == 2 and sys.argv[1] == "sm":
		print "Server mode!"
		server = tornado.web.Application([(r"/", RequestHandler), ])
		server.listen(8888)
		serverThread = Thread(target=tornado.ioloop.IOLoop.instance().start)
		serverThread.daemon = True
		serverThread.start()

	while True:
		print _queryParser(re.sub(r"\s+", "", raw_input("--> ").lower()))
