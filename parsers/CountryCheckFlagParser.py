# -*- coding: utf-8 -*-
from Parser import Parser
from PIL import Image

import io
import math
import operator
import re
import requests

class CountryCheckFlagParser(Parser):
	def __init__(self):
		super(CountryCheckFlagParser, self).__init__(r"^checkflag\((http://[0-9a-zA-Z_.\-\/]*(?:gif))\)$")
		with open("countries-names.txt") as handle:
			self.countriesNames = handle.read().splitlines()

		self.countriesNames.sort()

	def __call__(self, query):
		if self.wrapper(self.regex.match(query)):
			return self.__parse(self.wrapper.match.group(1))
		else:
			return False

	def __parse(self, url):
		refImage = self.__getImage(url)
		refImageHist = refImage.histogram()

		for countryName in self.countriesNames:
			image = self.__getImage("http://www.mapsofworld.com/images/world-countries-flags/" + countryName + "-flag.gif")
			imageHist = image.histogram()

			rms = math.sqrt(reduce(operator.add, map(lambda a, b: (a-b)**2, refImageHist, imageHist))/len(refImageHist))
			if rms <= 300:
				return re.sub("-", " ", countryName).title()

		return "Not found!"

	def __getImage(self, url):
		req = requests.get(url, stream=True)

		req.raise_for_status()

		req.raw.decode_content = True

		return Image.open(io.BytesIO(req.raw.read()))
		