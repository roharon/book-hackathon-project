import json
from os import environ

import requests

URL = "http://apis.data.go.kr/B551011/GoCamping/locationBasedList"


def fetch_suggest_campsite(longitude, latitude):
	params = {
		"pageNo": "1",
		"numOfRows": "100",
		"MobileOS": "ETC",
		"MobileApp": "AppTest",
		"serviceKey": environ['service_key'],
		"_type": "json",
		"mapX": longitude,
		"mapY": latitude,
		"radius": "30000"
	}

	response = requests.get(URL, params=params, verify=False)
	campsite_items = json.loads(response.text)['response']['body']['items']

	return campsite_items['item'] if campsite_items != "" else []
