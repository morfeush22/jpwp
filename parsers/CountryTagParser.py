# -*- coding: utf-8 -*-
from Parser import Parser

class CountryTagParser(Parser):
	def __init__(self, callback):
		super(CountryTagParser, self).__init__(r"^(country\([a-zA-Z]*\));?tag\(([0-9a-zA-Z_.,:]*)\)$")
		self.callback = callback

	def __call__(self, query):
		if self.wrapper(self.regex.match(query)):
			return self.__parse(self.wrapper.match.group(1), self.wrapper.match.group(2))
		else:
			return False

	def __parse(self, country, tag):
		_outputText = self.callback(country)
		_sentencesList = _outputText.split(".")

		return ". ".join([sentence for sentence in _sentencesList if sentence.find(tag) != -1]) + "."
		