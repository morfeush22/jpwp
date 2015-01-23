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
		req = requests.post(url, data=json.dumps(payload))

		req.raise_for_status()

		return (json.loads(req.text)["response"], json.loads(req.text)["type"])
		