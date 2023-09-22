import json
import logging
import os

import boto3
import requests
from botocore.exceptions import ClientError


def lambda_handler(event, context):
	aws_region = os.environ.get('AWS_REGION')
	admin_email = os.environ.get('admin_email')

	subject = "구글 드라이브 초대 주간 리포트"
	log = activity_log(os.environ.get('file_id'))
	body_html = "<h1>이메일 리포트 내용입니다</h1>\n{}".format(log)

	client = boto3.client('ses', region_name=aws_region)

	try:
		response = client.send_email(
			Destination={
				'ToAddresses': [
					admin_email
				]
			},
			Message={
				'Body': {
					'Html': {
						'Charset': 'UTF-8',
						'Data': body_html,
					},
				},
				'Subject': {
					'Charset': 'UTF-8',
					'Data': subject,
				},
			},
			Source=admin_email,
		)

		logging.info("Email sent! Message ID: {}".format(response['MessageId']))

		return {
			'statusCode': 200,
			'body': json.dumps(response)
		}

	except ClientError as e:
		logging.error(e.response['Error']['Message'])


def activity_log(file_id):
	url = 'https://driveactivity.googleapis.com/v2/activity:query'

	header = {
		"Content-Type": "application/json",
		"Authorization": "Bearer {}".format(get_token())
	}
	data = json.dumps({"ancestorName": "items/{}".format(file_id)})

	result = requests.post(url, data=data, headers=header)

	return result.json()


def get_token():
	headers = {
		"Content-Type": "application/x-www-form-urlencoded"
	}

	result = requests.post(
		"https://www.googleapis.com/oauth2/v4/token?client_id={}&client_secret={}&refresh_token={}".format(
			os.environ['client_id'],
			os.environ['client_secret'],
			os.environ['refresh_token']
		), headers=headers)

	if result.status_code == 200:
		result_json = result.json()
		return result_json['access_token']

	return None
