# -*- coding: utf-8 -*-
# ylnvsspc
# ylnvsspc1
from parsers import CountryParser, CountryTagParser, CountryJsonParser, CountryGetFlagParser, CountryCheckFlagParser
from pymongo import MongoClient
from threading import Thread

import json
import re
import requests
import sys
import tornado.escape
import tornado.ioloop
import tornado.web

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

class MakeRequest(object):
	def __init__(self):
		super(MakeRequest, self).__init__()
		
	def __call__(self, jsonQuery):
		url = "http://" + jsonQuery["address"] + ":" + jsonQuery["port"]
		payload = {"query": jsonQuery["content"], "type": jsonQuery["type"]}
		headers = {"content-type": "application/json"}
		req = requests.post(url, data=json.dumps(payload))

		req.raise_for_status()

		return json.loads(req.text)["response"]

class RequestHandler(tornado.web.RequestHandler):
	def initialize(self, queryParser):
		self.queryParser = queryParser

	def post(self):
		data = tornado.escape.json_decode(self.request.body)
		self.write(queryParser.parseHttpRequest(data["type"], data["query"]))

if __name__ == "__main__":
	client = MongoClient("mongodb://admin:admin@ds056727.mongolab.com:56727/countries")
	db = client.countries
	queryParser = ParseQuery(db)

	if len(sys.argv) == 2 and sys.argv[1] == "sm":
		print "Server mode!"
		server = tornado.web.Application([(r"/", RequestHandler, {"queryParser": queryParser}), ])
		server.listen(8888)
		serverThread = Thread(target=tornado.ioloop.IOLoop.instance().start)
		serverThread.daemon = True
		serverThread.start()

	while True:
		print queryParser.parseQuery(re.sub(r"\s+", "", raw_input("--> ").lower()))
