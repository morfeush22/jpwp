# -*- coding: utf-8 -*-
from Parser import Parser

class CountryJsonParser(Parser):
	def __init__(self, callback):
		super(CountryJsonParser, self).__init__(r"^([0-9a-zA-Z_]*)={([0-9a-zA-Z_,:;\(\)]+)}$")
		self.callback = callback
		self.variablesList = {}

	def __call__(self, query):
		if self.wrapper(self.regex.match(query)):
			return self.__parse(self.wrapper.match.group(1), self.wrapper.match.group(2))
		else:
			return False

	def __parse(self, variable, query):
		_address = _port = _type = _content = None

		self.variablesList[variable] = dict(_item.split(":") for _item in query.split(","))

		for _key, _value in self.variablesList[variable].iteritems():
			if _key == "address":
				_address = _value
			elif _key == "port":
				_port = _value
			elif _key == "type":
				_type = _value
			elif _key == "content":
				_content = _value
			else:
				raise ValueError("Wrong query!")

		print _address, _port, _type, _content

		if (_address and _port and _type and _content) is None:
			raise ValueError("Wrong query! None")

		_data = self.callback(_content)
			
		return _data
		# return self.variablesList[variable]
