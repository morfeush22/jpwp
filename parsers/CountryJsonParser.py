# -*- coding: utf-8 -*-
from Parser import Parser

import re
import requests

class CountryJsonParser(Parser):
	def __init__(self):
		super(CountryJsonParser, self).__init__(r"^([0-9a-zA-Z_]*)={([0-9a-zA-Z_.,:;\(\)]+)}$")
		self.variablesList = {}

	def __call__(self, query):
		if self.wrapper(self.regex.match(query)):
			return self.__parse(self.wrapper.match.group(1), self.wrapper.match.group(2))
		elif query in self.variablesList:
			return self.variablesList[query]
		else:
			return False

	def __parse(self, variable, query):
		address = port = queryType = content = None

		splitted = dict(item.split(":") for item in query.split(","))

		for key, value in splitted.iteritems():
			if key == "address":
				if not re.match(r"^(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$", value):
					raise ValueError("Wrong IP!")
				address = value
			elif key == "port":
				if not re.match(r"^0*(?:6553[0-5]|655[0-2][0-9]|65[0-4][0-9]{2}|6[0-4][0-9]{3}|[1-5][0-9]{4}|[1-9][0-9]{1,3}|[0-9])$", value):
					raise ValueError("Wrong port!")
				port = value
			elif key == "type":
				if not re.match(r"^(?:data|media)$", value):
					raise ValueError("Wrong type!")
				queryType = value
			elif key == "content":
				content = value
			else:
				raise ValueError("Wrong query!")

		if (address and port and queryType and content) is None:
			raise ValueError("Incomplete query!")

		self.variablesList[variable] = splitted
			
		return self.variablesList[variable]
