# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from Parser import Parser

import re
import urllib2
import unicodedata

class CountryParser(Parser):
	def __init__(self, db):
		super(CountryParser, self).__init__(r"^country\(([a-zA-Z'\s]*)\)$")
		self.db = db

	def __call__(self, query):
		if self.wrapper(self.regex.match(query)):
			return self.__parse(self.replaceTabs("_", self.wrapper.match.group(1).strip()))
		else:
			return False

	def __parse(self, country):
		contents = self.db.contents
		names = self.db.names

		getItem = names.find({"name": country})

		if getItem.count():
			return contents.find({"name_id": getItem[0]["_id"]})[0]["content"]
		else:
			url = "http://en.wikipedia.org/wiki/" + country
			try:
				rawHtml = urllib2.urlopen(url)
			except urllib2.HTTPError:
				raise Exception("{} - not found!".format(country))
				
			soup = BeautifulSoup(rawHtml)

			divId = {"id": re.compile("mw-content-text")}
			content = soup.find(attrs = divId)
			outputText = unicodedata.normalize("NFD", re.sub("\s+", " ", content.text).strip()) \
				.encode("ascii", "ignore")

			postName = {"name": country}
			postId = names.insert(postName)
			
			postContent = {"name_id": postId, "content": outputText}
			contents.insert(postContent)

			return outputText
