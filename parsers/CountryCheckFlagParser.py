# -*- coding: utf-8 -*-
from Parser import Parser
from PIL import Image

import io
import math
import re
import requests

class CountryCheckFlagParser(Parser):
	def __init__(self):
		super(CountryCheckFlagParser, self).__init__(r"^checkflag\((http://[0-9a-zA-Z'_.\-\/]*(?:gif))\)$")
		with open("country-flags-links.txt") as handle:
			self.countriesLinks = handle.read().splitlines()

	def __call__(self, query):
		if self.wrapper(self.regex.match(query)):
			return self.__parse(self.wrapper.match.group(1))
		else:
			return False

	def __parse(self, url):
		refImage = self.__getImage(url)
		refImageHist = refImage.histogram()

		for countryLink in self.countriesLinks:
			image = self.__getImage(countryLink)
			imageHist = image.histogram()

			rms = math.sqrt(sum((a-b)**2 for a, b in zip(refImageHist, imageHist))/len(refImageHist))
			if rms <= 300:
				return re.sub("-", " ", re.sub("_", " ", countryName)).title()

		return "Not found!"

	def __getImage(self, url):
		try:
			req = requests.get(url, stream=True)
		except requests.exceptions.ConnectionError:
			raise Exception("{} - not found!".format(url))

		try:	
			req.raise_for_status()
		except requests.exceptions.HTTPError:
			raise Exception("{} - not found!".format(url))
		
		req.raw.decode_content = True

		return Image.open(io.BytesIO(req.raw.read()))
		