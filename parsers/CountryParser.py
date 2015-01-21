# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from Parser import Parser

import urllib2
import unicodedata

class CountryParser(Parser):
	def __init__(self, db):
		super(CountryParser, self).__init__(r"^country\(([a-zA-Z]*)\)$")
		self.db = db

	def __call__(self, query):
		if self.wrapper(self.regex.match(query)):
			return self.__parse(self.wrapper.match.group(1))
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
