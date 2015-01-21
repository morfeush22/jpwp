# -*- coding: utf-8 -*-
import re

class Parser(object):
	def __init__(self, regex):
		super(Parser, self).__init__()
		self.regex = re.compile(regex)
		self.wrapper = MatchWrapper()

	def match(self, query):
		if self.regex.match(query):
			return True
		else:
			return False

class MatchWrapper(object):
	def __init__(self):
		super(MatchWrapper, self).__init__()
		self.match = None

	def __call__(self, item):
		self.match = item
		if self.match:
			return True
		else:
			return False
		