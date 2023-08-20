import datetime

from fetch_campsite import fetch_campsite
from fetch_suggest_campsite import fetch_suggest_campsite
from fetch_precipitation import fetch_precipitation


def search_campsite(weather_type, begins_at, ends_at):
	return _filter_campsites(fetch_campsite(), weather_type)


def search_suggest_campsite(weather_type, longitude, latitude, begins_at, ends_at):
	return _filter_campsites(fetch_suggest_campsite(longitude, latitude), weather_type)


def _filter_campsites(campsites, weather_type):
	current_time = datetime.datetime.now()

	seoul_weather_score = fetch_precipitation(current_time, "11B00000")
	gangwon_weather_score = fetch_precipitation(current_time, "11D10000")

	searchable_campsites = []
	for campsite in campsites:
		if campsite['doNm'] == "서울시" or campsite['doNm'] == "인천시" or campsite['doNm'] == "경기도":
			if ((weather_type == 'CLEAR' and seoul_weather_score < 75) or
					(weather_type == 'DOWNFALL' and seoul_weather_score >= 75)):
				searchable_campsites.append(_campsite_attribute(campsite))
		elif campsite['doNm'] == "강원도":
			if ((weather_type == 'CLEAR' and gangwon_weather_score < 75) or
					(weather_type == 'DOWNFALL' and gangwon_weather_score >= 75)):
				searchable_campsites.append(_campsite_attribute(campsite))
		else:
			searchable_campsites.append(_campsite_attribute(campsite))

	return searchable_campsites

def _campsite_attribute(campsite):
	return {
		"name": campsite['facltNm'],
		"allar": int(campsite['allar']),
		"line_intro": campsite['lineIntro'],
		"image_url": campsite['firstImageUrl'],
		"created_time": _iso8601_format(campsite['createdtime']),
		"updated_time": _iso8601_format(campsite['modifiedtime']),
		"address": campsite['addr1'],
		"latitude": campsite['mapY'],
		"longitude": campsite['mapX'],
	}


def _iso8601_format(text):
	return datetime.datetime.strptime(text, "%Y-%m-%d %H:%M:%S").isoformat()
