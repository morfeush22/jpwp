# -*- coding: utf-8 -*-
from Parser import Parser
from PIL import Image
from scipy.signal.signaltools import correlate2d as c2d

import io
import math
import numpy
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
		"""
		refImage = self.__getImage(url)
		refImageArr = numpy.asarray(refImage)
		refImageNorm = (refImageArr-refImageArr.mean())/refImageArr.std()
		
		for countryLink in self.countriesLinks:
			image = self.__getImage(countryLink)
			imageArr = numpy.asarray(image)
			imageNorm = (imageArr-imageArr.mean())/imageArr.std()

			corr = c2d(refImageNorm, imageNorm, mode="same")
			print corr

			if corr > 50000:
				return re.sub("-", " ", re.sub("_", " ",  re.match(r"^(.*)-(?:flag)?.*$", countryLink.rsplit("/", 1)[1]).group(1))).title()
			
		"""
		refImage = self.__getImage(url)
		refImageHist = refImage.histogram()

		for countryLink in self.countriesLinks:
			image = self.__getImage(countryLink)
			imageHist = image.histogram()

			rms = math.sqrt(sum((a-b)**2 for a, b in zip(refImageHist, imageHist))/len(refImageHist))
			if rms <= 1000:
				return re.sub("-", " ", re.sub("_", " ",  re.match(r"^(.*)-(?:flag)?.*$", countryLink.rsplit("/", 1)[1]).group(1))).title()
		
		return "Not found!"

	def __getImage(self, url):
		try:
			req = requests.get(url, stream=True)
		except requests.exceptions.ConnectionError:
			raise Exception("{} - connection problem!".format(url))

		try:	
			req.raise_for_status()
		except requests.exceptions.HTTPError:
			raise Exception("{} - url not found!".format(url))
		
		req.raw.decode_content = True

		return Image.open(io.BytesIO(req.raw.read()))
		