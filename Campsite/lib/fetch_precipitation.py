import json
import requests
from os import environ

URL = "http://apis.data.go.kr/1360000/MidFcstInfoService/getMidLandFcst"

# 예보구역코드
# 11B00000	서울, 인천, 경기도
# 11D10000	강원도영서
# 11D20000	강원도영동
# 11C20000	대전, 세종, 충청남도
# 11C10000	충청북도
# 11F20000	광주, 전라남도
# 11F10000	전라북도
# 11H10000	대구, 경상북도
# 11H20000	부산, 울산, 경상남도
# 11G00000	제주도


def fetch_precipitation(begins_at, reg_id):
	params = {
		"pageNo": "1",
		"numOfRows": "1",
		"regId": reg_id,
		"tmFc": begins_at.strftime("%Y%m%d0600"),
		"serviceKey": environ['service_key'],
		"dataType": "JSON"
	}

	response = requests.get(URL, params=params, verify=False)
	weather = json.loads(response.text)['response']['body']['items']['item'][0]

	return _precipitation_score(weather)


def _precipitation_score(weather):
	score = (weather['rnSt3Pm'] + weather['rnSt4Pm'] + weather['rnSt5Pm'] + weather['rnSt6Pm'] + weather['rnSt7Pm'] +
	         weather['rnSt8'] + weather['rnSt9'])

	return score / 7
