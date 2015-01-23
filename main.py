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
		print "Server mode"
		server = tornado.web.Application([(r"/", RequestHandler, {"queryParser": queryParser}), ])
		server.listen(8888)
		serverThread = Thread(target=tornado.ioloop.IOLoop.instance().start)
		serverThread.daemon = True
		serverThread.start()
	else:
		print "To run in server mode, start with 'sm' flag"

	while True:
		try:
			queryParser.parseQuery(raw_input("--> ").lower().strip())
		except UserWarning:
			print "Example use: \
			country(Poland) \
			country(Poland); tag(marriage) \
			country(Poland); getflag \
			checkflag(http://foo.bar/flag.gif) \
			data = { \
				address: 127.0.0.1, \
				port: 8888, \
				type: media \
				content: country(Poland); getflag}"
