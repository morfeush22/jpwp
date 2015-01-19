# -*- coding: utf-8 -*-
# ylnvsspc
# ylnvsspc1

import urllib2
import re
from bs4 import BeautifulSoup
from pymongo import MongoClient

class ParseQuery(object):
	def __init__(self, db):
		self.countryQueryRe = re.compile(r"^country\(([a-zA-Z]*)\)$")
		self.countryTagQueryRe = re.compile(r"^country\(([a-zA-Z]*)\);?tag\(([0-9a-zA-Z_.,:]*)\)$")
		self.countryGetFlagQueryRe = re.compile(r"^country\(([a-zA-Z]*)\);?getflag$")
		self.countryCheckFlagRe = re.compile(r"^checkflag\((http://[0-9a-zA-Z_.]*[gif|jpeg])\)$")
		self.countryJson = re.compile(r"^([0-9a-zA-Z_]*)={([0-9a-zA-Z_,:]+)}$")

		self.db = db

	def __call__(self, query):
		wrapper = MatchWrapper()
		if wrapper(self.countryQueryRe.match(query)):
			# get country info from wiki
			country = wrapper.match.group(1)
			print self.__getCountry(country)	
		elif wrapper(self.countryTagQueryRe.match(query)):
			# get country info from wiki and get sentences with tags
			country = wrapper.match.group(1)
			tag = wrapper.match.group(2)
			print self.__getCountryTag(country, tag)
		elif wrapper(self.countryGetFlagQueryRe.match(query)):
			# return flag
			country = wrapper.match.group(1)
			self.__getCountryFlag(country)
		elif wrapper(self.countryCheckFlagRe.match(query)):
			# check flag
			url = wrapper.match.group(1)
			self.__checkCountryFlag(url)
		elif wrapper(self.countryJson.match(query)):
			# json query
			variable = wrapper.match.group(1)
			query = wrapper.match.group(2)
			self.__handleJsonQuery(variable, query)
		else:
			# how to query
			print "???"

	def __getCountry(self, country):
		contents = self.db.contents
		names = self.db.names

		getItem = names.find({"name": country})
		if getItem.count():
			return contents.find({"name_id": getItem[0]["_id"]})[0]["content"]
		else:
			url = "http://en.wikipedia.org/wiki/" + country
			rawHtml = urllib2.urlopen(url)
			soup = BeautifulSoup(rawHtml)

			divId = {"id": re.compile("mw-content-text")}
			content = soup.find(attrs = divId)
			outputText = re.sub("\s+", " ", content.text).strip()

			postName = {"name": country}
			postId = names.insert(postName)
			
			postContent = {"name_id": postId, "content": outputText}
			contents.insert(postContent)

			return outputText

	def __getCountryTag(self, country, tag):
		outputText = getCountry(country)
		# + tag
		pass

	def __getCountryFlag(self, country):
		pass

	def __checkCountryFlag(self, imageUrl):
		pass

	def __handleJsonQuery(self, variable, query):
		pass

class MatchWrapper(object):
	def __init__(self):
		self.match = None

	def __call__(self, item):
		if item:
			self.match = item
			return True
		else:
			return False

if __name__ == "__main__":

	client = MongoClient("mongodb://admin:admin@ds056727.mongolab.com:56727/countries")
	db = client.countries
	queryParser = ParseQuery(db)

	while True:
		print "Go on"
		queryParser(re.sub(r"\s+", "", raw_input().lower()))

	print client
	print db

	"""
	file_ = open('text.txt', 'w')
	file_.write(outputText.encode("utf-8"))
	file_.close
	"""