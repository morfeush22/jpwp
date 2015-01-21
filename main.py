# -*- coding: utf-8 -*-
# ylnvsspc
# ylnvsspc1
from parsers import ParseQuery
from pymongo import MongoClient
from threading import Thread

import json
import re
import sys
import tornado.escape
import tornado.ioloop
import tornado.web

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
