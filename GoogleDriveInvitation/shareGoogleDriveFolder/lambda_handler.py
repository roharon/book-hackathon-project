import json
import logging
import os
import re

import requests


def lambda_handler(event, _context):
	try:
		body = json.loads(event['body'])
		email = body['email']
		verify_code = body['verify_code']

		share(email, verify_code)

		return {
			"statusCode": 201
		}
	except Exception as e:
		logging.info(e)

		return {
			"statusCode": 400
		}


def share(email=None, verify_code=None):
	email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
	if not re.fullmatch(email_regex, email):
		return RuntimeError("email 형식이 올바르지 않습니다.")

	if verify_code != os.environ.get('VERIFY_CODE'):
		return RuntimeError("verify_code가 일치하지 않습니다.")

	file_id = os.environ.get('FILE_ID')
	if file_id is None:
		return RuntimeError("file_id가 없습니다.")

	token = get_token()

	if token is None:
		return RuntimeError("token을 가져올 수 없습니다.")

	header = {
		"Content-Type": "application/json",
		"Authorization": "Bearer {}".format(token)
	}

	data = json.dumps({
		"role": os.environ.get('GOOGLE_DRIVE_ROLE'),
		"type": "user",
		"emailAddress": email
	})
	permission_url = (
		"https://www.googleapis.com/drive/v3/files/{file_id}/permissions?emailMessage={message}"
		.format(file_id=file_id, message='공유 문서함에 구성원이 추가되었습니다.'))
	res = requests.post(permission_url, headers=header, data=data)

	if res.status_code != 200:
		raise RuntimeError("공유 폴더 초대에 실패하였습니다.")

	return res.json()


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
