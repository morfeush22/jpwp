# -*- coding: utf-8 -*-
# ylnvsspc
# ylnvsspc1

import urllib2
import re
from bs4 import BeautifulSoup
from pymongo import MongoClient

class ParseQuery(object):
	def __init__(self):
		self.countryQueryRe = re.compile(r"^country\(([a-zA-Z]*)\)$")
		self.countryTagQueryRe = re.compile(r"^country\(([a-zA-Z]*)\);?tag\(([0-9a-zA-Z_.,:]*)\)$")
		self.countryGetFlagQueryRe = re.compile(r"^country\(([a-zA-Z]*)\);?getflag$")
		self.countryCheckFlagRe = re.compile(r"^checkflag\((http://[0-9a-zA-Z_.]*[gif|jpeg])\)$")
		self.countryJson = re.compile(r"^([0-9a-zA-Z_]*)={([0-9a-zA-Z_,:]+)}$")

	def __call__(self, query):
		wrapper = Wrapper()
		if wrapper(self.countryQueryRe.match(query)):
			# get country info from wiki
			country = wrapper.match.group(1)
			getCountry(country)	
		elif wrapper(self.countryTagQueryRe.match(query)):
			# get country info from wiki and get sentences with tags
			country = wrapper.match.group(1)
			tag = wrapper.match.group(2)
			getCountryTag(country, tag)
		elif wrapper(self.countryGetFlagQueryRe.match(query)):
			# return flag
			country = wrapper.match.group(1)
			getCountryFlag(country)
		elif wrapper(self.countryCheckFlagRe.match(query)):
			# check flag
			url = wrapper.match.group(1)
			checkCountryFlag(url)
		elif wrapper(self.countryJson.match(query)):
			# json query
			variable = wrapper.match.group(1)
			query = wrapper.match.group(2)
			handleJsonQuery(variable, query)
		else:
			# how to query
			print "???"

class Wrapper(object):
	def __init__(self):
		self.match = None

	def __call__(self, regex):
		if regex:
			self.match = regex
			return True
		else:
			return False

def getCountry(country):
	url = "http://en.wikipedia.org/wiki/" + country
	rawHtml = urllib2.urlopen(url)
	soup = BeautifulSoup(rawHtml)

	divId = {"id": re.compile("mw-content-text")}
	content = soup.find(attrs = divId)
	outputText = re.sub("\s+", " ", content.text).strip()

	return outputText

def getCountryTag(country, tag):
	getCountry(country)
	# + tag
	pass

def getCountryFlag(country):
	pass

def checkCountryFlag(imageUrl):
	pass

def handleJsonQuery(variable, query):
	pass

if __name__ == "__main__":

	client = MongoClient("mongodb://admin:admin@ds056727.mongolab.com:56727/countries")
	db = client.countries
	queryParser = ParseQuery()

	while True:
		queryParser(re.sub(r"\s+", "", raw_input()))

	print client
	print db

	"""
	file_ = open('text.txt', 'w')
	file_.write(outputText.encode("utf-8"))
	file_.close
	"""