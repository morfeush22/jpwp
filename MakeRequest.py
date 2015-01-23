# -*- coding: utf-8 -*-
import json
import requests

class MakeRequest(object):
	def __init__(self):
		super(MakeRequest, self).__init__()
		
	def __call__(self, jsonQuery):
		url = "http://" + jsonQuery["address"] + ":" + jsonQuery["port"]
		payload = {"query": jsonQuery["content"], "type": jsonQuery["type"]}
		headers = {"content-type": "application/json"}
		try:
			req = requests.post(url, data=json.dumps(payload), headers=headers)
		except requests.exceptions.ConnectionError:
			raise Exception("{}:{} - not found!".format(jsonQuery["address"], jsonQuery["port"]))
			
		try:
			req.raise_for_status()
		except requests.exceptions.HTTPError:
			raise Exception("{}:{} - file not found!".format(jsonQuery["address"], jsonQuery["port"]))

		return (json.loads(req.text)["response"], json.loads(req.text)["type"])
		