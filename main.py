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
		try:
			resp = queryParser.parseHttpRequest(data["type"], data["query"])
			self.write(resp)
		except Exception as e:
			self.write({"response": "Bad request!", "type": "data"})

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
			inp = raw_input("--> ").lower().strip()
			queryParser.parseQuery(inp)
		except UserWarning:
			print "Example use:\n" + \
				"\ncountry(Poland)\n" + \
				"country(Poland); tag(marriage)\n" + \
				"country(Poland); getflag\n" + \
				"checkflag(http://foo.bar/flag.gif)\n" + \
				"data = {\n" + \
					"\taddress: 127.0.0.1,\n" + \
					"\tport: 8888,\n" + \
					"\ttype: media,\n" + \
					"\tcontent: country(Poland); getflag \n" + \
					"\t} \n"
		except Exception as e:
			print str(e)
