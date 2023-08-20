import json
from os import environ
import requests

URL = "https://apis.data.go.kr/B551011/GoCamping/basedList"


def fetch_campsite():
	params = {
		"pageNo": "1",
		"numOfRows": "100",
		"MobileOS": "ETC",
		"MobileApp": "AppTest",
		"serviceKey": environ['service_key'],
		"_type": "json"
	}

	response = requests.get(URL, params=params)
	campsites = json.loads(response.text)['response']['body']['items']['item']

	return campsites
