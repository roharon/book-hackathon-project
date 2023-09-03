#!/usr/bin/env python
import datetime
import json

import requests


def to_datetime(time_ms: int) -> str:
	dt = datetime.datetime.fromtimestamp(time_ms // 1000)
	return "{}T{}Z".format(str(dt.date()), str(dt.time()))


class TRKPoint:
	def __init__(self, time: int, latitude=None, longitude=None, ele=None):
		self.time = time
		self.latitude = latitude
		self.longitude = longitude
		self.element = ele

	def __str__(self):
		return """<trkpt lat="{}" lon="{}">
    <ele>{}</ele>
    <time>{}</time>
   </trkpt>
   """.format(self.latitude, self.longitude, self.element, to_datetime(self.time))


def to_gpx(data):
	GPX_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
	<gpx creator="NRC to Strava" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd" version="1.1" xmlns="http://www.topografix.com/GPX/1/1"
		<metadata>
			<time>{}</time>
		</metadata>
		<trk>
			<name>{}</name>
			<type>9</type>
			<trkseg>{}</trkseg>
		</trk>
	</gpx>
	"""

	name = data['tags']['com.nike.name']
	start_time = to_datetime(data['start_epoch_ms'])

	for metric in data['metrics']:
		if metric['type'] == 'latitude':
			lat_values = metric['values']
		if metric['type'] == 'longitude':
			lon_values = metric['values']
		if metric['type'] == 'elevation':
			ele_values = metric['values']

	points = []
	for location_index in range(len(lat_values)):
		latitude = lat_values[location_index]
		longitude = lon_values[location_index]

		if latitude['start_epoch_ms'] != longitude['start_epoch_ms']:
			pass

		point = TRKPoint(time=latitude['start_epoch_ms'], latitude=latitude['value'], longitude=longitude['value'])
		points.append(point)

	element_index = 0
	for point_index in range(len(points)):
		point_time = points[point_index].time
		while True:
			if ele_values[element_index]['start_epoch_ms'] >= point_time:
				points[point_index].element = ele_values[element_index]['value']
				break
			else:
				element_index += 1

	return GPX_TEMPLATE.format(start_time, name, "".join([str(point) for point in points]))


def fetch_activity_to_gpx(activity_id: str, access_token: str) -> str:
	nike_activity_url = 'https://api.nike.com/sport/v3/me/activity/{}?metrics=ALL'.format(activity_id)
	headers = {
		'Authorization': 'Bearer {}'.format(access_token)
	}

	response = requests.request("GET", nike_activity_url, headers=headers)

	return to_gpx(json.loads(response.text))


def fetch_activity_ids(access_token: str) -> str:
	nike_activity_list_url = 'https://api.nike.com/sport/v3/me/activities/before_time/{}'.format(
		int(datetime.datetime.now().timestamp() * 1000))

	headers = {
		'Authorization': 'Bearer {}'.format(access_token)
	}

	response = requests.request("GET", nike_activity_list_url, headers=headers)

	activities = response.json()["activities"]
	return [item["id"] for item in activities]
