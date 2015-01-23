# -*- coding: utf-8 -*-
from Parser import Parser

class CountryTagParser(Parser):
	def __init__(self, countryParser):
		super(CountryTagParser, self).__init__(r"^(country\([a-zA-Z\s]*\));\s*tag\(([0-9a-zA-Z_.,:\s]*)\)$")
		self.countryParser = countryParser

	def __call__(self, query):
		if self.wrapper(self.regex.match(query)):
			return self.__parse(self.wrapper.match.group(1), self.replaceTabs(" ", self.wrapper.match.group(2).strip()))
		else:
			return False

	def __parse(self, country, tag):
		outputText = self.countryParser(country)
		sentencesList = outputText.split(".")

		result = ". ".join([sentence for sentence in sentencesList if sentence.lower().find(tag) != -1]) + "."
		if result == ".":
			return "Found nothing!"

		return result
		