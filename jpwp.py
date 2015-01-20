# -*- coding: utf-8 -*-
# ylnvsspc
# ylnvsspc1

import urllib2
import re
import unicodedata
from bs4 import BeautifulSoup
from pymongo import MongoClient

class ParseQuery(object):
	def __init__(self, db):
		self.countryQueryRe = re.compile(r"^country\(([a-zA-Z]*)\)$")
		self.countryTagQueryRe = re.compile(r"^country\(([a-zA-Z]*)\);?tag\(([0-9a-zA-Z_.,:]*)\)$")
		self.countryGetFlagQueryRe = re.compile(r"^country\(([a-zA-Z]*)\);?getflag$")
		self.countryCheckFlagRe = re.compile(r"^checkflag\((http://[0-9a-zA-Z_.]*[gif|jpeg])\)$")
		self.countryJson = re.compile(r"^([0-9a-zA-Z_]*)={([0-9a-zA-Z_,:;\(\)]+)}$")

		self.variablesList = {}
		self.db = db

	def __call__(self, query):
		wrapper = MatchWrapper()
		if wrapper(self.countryQueryRe.match(query)):
			# get country info from wiki
			country = wrapper.match.group(1)
			return self.__getCountry(country)	
		elif wrapper(self.countryTagQueryRe.match(query)):
			# get country info from wiki and get sentences with tags
			country = wrapper.match.group(1)
			tag = wrapper.match.group(2)
			return self.__getCountryTag(country, tag)
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
			return self.__handleJsonQuery(variable, query)
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
			outputText = unicodedata.normalize("NKFD", re.sub("\s+", " ", content.text).strip()) \
				.encode("ascii", "ignore")

			postName = {"name": country}
			postId = names.insert(postName)
			
			postContent = {"name_id": postId, "content": outputText}
			contents.insert(postContent)

			return outputText

	def __getCountryTag(self, country, tag):
		outputText = self.__getCountry(country)
		sentencesList = outputText.split(".")

		return ". ".join([sentence for sentence in sentencesList if sentence.find(tag) != -1]) + "."

	def __getCountryFlag(self, country):
		pass

	def __checkCountryFlag(self, imageUrl):
		pass

	def __handleJsonQuery(self, variable, query):
		# print item, value for query.split(",")
		# data={address:adr,port:prt,type:tp,content:country(poland);tag(marriage)}
		address_ = port_ = type_ = content_ = None

		self.variablesList[variable] = dict(item.split(":") for item in query.split(","))
		for key, value in self.variablesList[variable].iteritems():
			if key == "address":
				address_ = value
			elif key == "port":
				port_ = value
			elif key == "type":
				type_ = value
			elif key == "content":
				content_ = value
			else:
				# throw
				return

		if (address_ and port_ and type_ and content_) is None:
			# throw
			return

		data = self.__call__(content_)
			
		return self.variablesList[variable]

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
		print queryParser(re.sub(r"\s+", "", raw_input().lower()))

	"""
	file_ = open('text.txt', 'w')
	file_.write(outputText.encode("utf-8"))
	file_.close
	"""
