# -*- coding: utf-8 -*-
from Parser import Parser

import re

class CountryJsonParser(Parser):
	def __init__(self, callback):
		super(CountryJsonParser, self).__init__(r"^([0-9a-zA-Z_]*)={([0-9a-zA-Z_.,:;\(\)]+)}$")
		self.callback = callback
		self.variablesList = {}

	def __call__(self, query):
		if self.wrapper(self.regex.match(query)):
			return self.__parse(self.wrapper.match.group(1), self.wrapper.match.group(2))
		elif query in self.variablesList:
			return self.variablesList[query]
		else:
			return False

	def __parse(self, variable, query):
		_address = _port = _type = _content = None

		_splitted = dict(_item.split(":") for _item in query.split(","))

		for _key, _value in _splitted.iteritems():
			if _key == "address":
				if not re.match(r"^(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$", _value):
					raise ValueError("Wrong IP!")
				_address = _value
			elif _key == "port":
				if not re.match(r"^0*(?:6553[0-5]|655[0-2][0-9]|65[0-4][0-9]{2}|6[0-4][0-9]{3}|[1-5][0-9]{4}|[1-9][0-9]{1,3}|[0-9])$", _value):
					raise ValueError("Wrong port!")
				_port = _value
			elif _key == "type":
				if not re.match(r"^(?:data|media)$", _value):
					raise ValueError("Wrong type!")
				_type = _value
			elif _key == "content":
				_content = _value
			else:
				raise ValueError("Wrong query!")

		if (_address and _port and _type and _content) is None:
			raise ValueError("Incomplete query!")

		self.variablesList[variable] = _splitted

		# _data = self.callback(_content)
			
		return self.variablesList[variable]
