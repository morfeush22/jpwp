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
		_contents = self.db.contents
		_names = self.db.names

		_getItem = _names.find({"name": country})

		if _getItem.count():
			return _contents.find({"name_id": _getItem[0]["_id"]})[0]["content"]
		else:
			_url = "http://en.wikipedia.org/wiki/" + country
			_rawHtml = urllib2.urlopen(_url)
			_soup = BeautifulSoup(_rawHtml)

			_divId = {"id": re.compile("mw-content-text")}
			_content = _soup.find(attrs = _divId)
			_outputText = unicodedata.normalize("NKFD", re.sub("\s+", " ", _content.text).strip()) \
				.encode("ascii", "ignore")

			_postName = {"name": country}
			_postId = _names.insert(_postName)
			
			_postContent = {"name_id": _postId, "content": _outputText}
			_contents.insert(_postContent)

			return _outputText
