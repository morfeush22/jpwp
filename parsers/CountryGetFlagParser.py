# -*- coding: utf-8 -*-
from Parser import Parser

import re
import requests

class CountryGetFlagParser(Parser):
	def __init__(self):
		super(CountryGetFlagParser, self).__init__(r"^country\(([a-zA-Z'\s]*)\);\s*getflag$")
		with open("country-flags-links.txt") as handle:
			self.countriesLinks = handle.read().splitlines()
		
	def __call__(self, query):
		if self.wrapper(self.regex.match(query)):
			return self.__parse(self.replaceTabs(" ", self.wrapper.match.group(1).strip()))
		else:
			return False

	def __parse(self, country):
		dashSub = ".*" + re.sub(" ", "-", country) + ".*"
		underscoreSub = ".*" + re.sub(" ", "_", country) + ".*"

		for countryLink in self.countriesLinks:
			if re.match(dashSub, countryLink, re.IGNORECASE) or re.match(underscoreSub, countryLink, re.IGNORECASE):
				try:
					req = requests.get(countryLink, stream=True)
				except requests.exceptions.ConnectionError:
					raise Exception("{} - connection problem!".format(countryLink))
				
				try:
					req.raise_for_status()
				except requests.exceptions.HTTPError:
					raise Exception("{} - url not found!".format(countryLink))

				req.raw.decode_content = True

				return req.raw.read()


		return None
