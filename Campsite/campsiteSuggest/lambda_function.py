import logging
import json

from lib.search_campsite import search_suggest_campsite


def lambda_handler(event, context):
	logging.info(event)
	result = search_suggest_campsite('CLEAR',
	                                 latitude=event['queryStringParameters']['latitude'],
	                                 longitude=event['queryStringParameters']['longitude'],
	                                 begins_at=event['queryStringParameters']['begins_at'],
	                                 ends_at=event['queryStringParameters']['ends_at'])

	return {
		'statusCode': 200,
		'body': json.dumps(result, ensure_ascii=False)
	}
