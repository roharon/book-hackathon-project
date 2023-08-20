import logging
from lib.search_campsites import search_campsite


def lambda_handler(event, context):
	logging.info(event)
	result = search_campsite(None, None)
	return {
		'statusCode': 200,
		'body': result
	}
